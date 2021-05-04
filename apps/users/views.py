import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import ListView
from django.views.generic import View
from django.views.generic.edit import FormView

from apps.accounts.forms import CustomUserCreationForm, CustomLogin, MyProfileForm, CheckPartnerCodeForm
from apps.accounts.models import CustomUser, Credit, Company_infos
from apps.accounts.services import add_subscribers
from apps.deas.services import post_song_from_url
from apps.logger.services import Logger
from apps.music.forms import SongUploadForm, UpdateSongForm
from apps.music.models import Song
from apps.songpkg.forms import Songpkg
from .forms import AddressChangeForm

logger = logging.getLogger(__name__)
db_logger = Logger()

@require_POST
def login(request):
    if request.method == 'POST':
        login_form = CustomLogin(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            if(request.user.is_partner and request.user.approved_partner):
                return JsonResponse({'is_partner': True}, status=200)
            else:
                return JsonResponse({})
        else:
            return JsonResponse({'errors': login_form.errors}, status=401)


@require_GET
def logout(request):
    django_logout(request)
    return redirect('home')


@csrf_exempt
@require_POST
def register(request):
    if request.method == "POST":
        register_form = CustomUserCreationForm(request.POST, request.FILES)

        if register_form.is_valid():
            new_register_form = CustomUserCreationForm(request.POST)  # Filepath uses the user's ID but it doesn't exist yet
            user = new_register_form.save()
            user.is_active = True

            referrer_code = request.POST.get('referrer_code', None)
            if referrer_code:
                referrer = CustomUser.objects.filter(referral_code=referrer_code).first()
                user.referrer = referrer

            if request.FILES.get("profile_picture", None):
                user.profile_picture = request.FILES.get("profile_picture")

            user.save()
            auth_login(request, user)
            return JsonResponse({})
        else:
            return JsonResponse({'errors': register_form.errors}, status=400)


class MyAccountOverview(LoginRequiredMixin, ListView):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'
    template_name = 'pages/myAccount/myAccountOverview.html'
    success_message = None
    paginate_by = 20
    context_object_name = 'songs'

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', None)
        order_direction = self.request.GET.get('direction', None)

        queryset = Song.objects.filter(user=self.request.user, active=True)
        if order_by:
            if order_by == 'title':
                queryset = queryset.order_by(Lower(order_by).desc()) if order_direction == 'desc' else queryset.order_by(Lower(order_by))
            elif order_by == 'rank':
                queryset = sorted(queryset, key=lambda i: i.rank(), reverse=True) if order_direction == 'desc' else sorted(queryset, key=lambda i: i.rank())
            else:
                if order_direction == 'desc':
                    order_by = '-' + order_by
                queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyAccountOverview, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', None)
        context['direction'] = self.request.GET.get('direction', None)
        return context


class MyAccountProfile(LoginRequiredMixin,View):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'

    template = 'pages/myAccount/myAccountMyProfile.html'
    success_message = None

    def get(self, request):
        profile_form = MyProfileForm(instance=request.user)
        return render(request, self.template, {'profile_form':profile_form})

    def post(self, request):
        err = False
        profile_form = MyProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _('Operation performed with success'))
        else:
            db_logger.new_logger(request, type="errors", description=_('Update Profile Operation failure !'))
            messages.error(request, _('Operation failure !'))
            err = True

        return render(request, self.template, {'profile_form':profile_form, 'error':err})


class MyPasswordEdit(LoginRequiredMixin,View):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'

    template = 'pages/myAccount/myAccountAccount.html'
    success_message = None

    def get(self, request):
        password_form = PasswordChangeForm(request.user)
        return render(request, self.template, {'password_form': password_form})

    def post(self, request):
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
        else:
            db_logger.new_logger(request, type="errors", description=_('Update Password : Please correct the error below.'))
            messages.error(request, _('Please correct the error below.'))

        return render(request, self.template, {'password_form': password_form})


class MyCredit(LoginRequiredMixin,View):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'

    template = 'pages/myAccount/myAccountMyCredits.html'
    success_message = None

    def get(self, request):
        credit = Credit()
        return render(request, self.template, {'COMPLETE_STATUS': credit.COMPLETED})

    def post(self, request):
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
        else:
            db_logger.new_logger(request, type="errors", description=_('Update Password : Please correct the error below.'))
            messages.error(request, _('Please correct the error below.'))

        return render(request, self.template, {'password_form': password_form})


class Invoice(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    template = 'invoice.html'
    def get(self, request):
        pk_credit = request.GET.get('id',None)
        invoice = Credit.objects.get(pk=pk_credit)

        invoice_tax=[]
        amount_without_tax = invoice.payment_amount

        if invoice.tax_data:
            for tax in invoice.tax_data['tax_type'].split(','):
                invoice_tax.append({tax:invoice.tax_data[tax+"_amount"]})
            amount_without_tax = invoice.tax_data["price_without_taxes"]

        return render(request, self.template, {
            'compagny_info':Company_infos.objects.all().first(),
            'invoice_tax':invoice_tax,
            'amount_without_tax':amount_without_tax,
            'package':Songpkg.objects.filter(nbofcredits=invoice.credit_amount).first(),"invoice_data":invoice})

class MyCreditPackage(LoginRequiredMixin,View):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'

    template = 'pages/myAccount/myAccountCreditsPackages.html'
    success_message = None

    def get(self, request):
        return render(request, self.template, {
            'list_package': Songpkg.objects.all(),
            'paypal_client_id': settings.PAYPAL_API_CLIENTID
        })

    def post(self, request):
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
        else:
            db_logger.new_logger(request, type="errors", description=_('Update Password : Please correct the error below.'))
            messages.error(request, _('Please correct the error below.'))

        return render(request, self.template, {'password_form': password_form})


class Uploadmusic(LoginRequiredMixin,View):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'

    template = 'pages/myAccount/myAccountUploadArtwork.html'
    success_message = None

    def get(self, request):
        if request.user.credit_available <= 0:
            db_logger.new_logger(request, type="errors", description=_('Credit Package : Credits are required before performing this action.'))
            messages.error(request, _('Credits are required before performing this action.'))
            return redirect('creditpackage')
        upload_form = SongUploadForm()
        return render(request, self.template, {'upload_form':upload_form})

    def post(self, request):
        if request.user.credit_available <= 0:
            db_logger.new_logger(request, type="errors", description=_('Credit Package : Credits are required before performing this action.'))
            messages.error(request, _('Credits are required before performing this action.'))
            return redirect('creditpackage')
        upload_form = SongUploadForm(data=request.POST, files=request.FILES)

        if upload_form.is_valid():
            credit_available = int(request.user.credit_available) - 1
            if credit_available >= 0:
                song = upload_form.save(commit=False)
                song.user = request.user
                song.save()

                deas_id = upload_song_for_analysis(song, request)
                if deas_id:
                    song.deas_id = deas_id
                    song.analysis_status = Song.PROCESSING
                    song.save()
                    request.user.credit_available = credit_available
                    request.user.save()
                    messages.success(request, _('Upload completed successfully !'))
                    upload_form = SongUploadForm()
                else:
                    song.delete()  # "Dumb" recovery, maybe some better retrying options in the future
                    db_logger.new_logger(request, type="errors", description=_('Song could not be sent for analysis, please try again .'))
                    messages.error(request, _('Song could not be sent for analysis, please try again .'))

            else:
                db_logger.new_logger(request, type="errors", description=_("You don't have enough credit to perform this action ."))
                messages.error(request, _("You don't have enough credit to perform this action ."))
                return redirect('creditpackage')
        else:
            db_logger.new_logger(request, type="errors", description=_("Upload Music: Please correct the error below."))
            messages.error(request, _('Please correct the error below.'))

        if request.is_ajax():
            return render(request, '_upload_form.html', {'upload_form': upload_form})
        else:
            return render(request, self.template, {'upload_form': upload_form})


class Updatesonginfo(LoginRequiredMixin,View):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'

    template = 'pages/myAccount/myAccountUploadArtwork.html'
    success_message = None

    def get(self, request, song_id=None):
        if song_id:
            songs = get_object_or_404(Song, user=request.user, active=True, pk=song_id)
            upload_form = UpdateSongForm(instance=songs)
            return render(request, self.template, {'upload_form':upload_form, 'song_id': song_id})
        else:
            db_logger.new_logger(request, type="errors", description=_("There is not song_id value"))


    def post(self, request, song_id=None):
        if song_id:
            songs = get_object_or_404(Song, user=request.user, active=True, pk=song_id)
            upload_form = UpdateSongForm(instance=songs, data=request.POST, files=request.FILES)

            if upload_form.is_valid():
                song = upload_form.save(commit=False)
                song.user = request.user
                song.save()
                messages.success(request, _('Update completed successfully !'))
                return redirect('uploadmusic')
            else:
                db_logger.new_logger(request, type="errors", description=_("Update song Infos: Please correct the error below."))
                messages.error(request, _('Please correct the error below.'))

            if request.is_ajax():
                return render(request, '_upload_form.html', {'upload_form': upload_form,  'song_id': song_id})
            else:
                return render(request, self.template, {'upload_form': upload_form,  'song_id': song_id})
        else:
            db_logger.new_logger(request, type="errors", description=_("There is not song_id value"))


class MySong(LoginRequiredMixin,ListView):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'
    success_message = None
    paginate_by = 20
    template_name = 'pages/myAccount/myAccountMySongs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', None)
        order_direction = self.request.GET.get('direction', None)

        queryset = Song.objects.filter(user=self.request.user, active=True)
        if order_by:
            if order_by == 'title':
                queryset = queryset.order_by(Lower(order_by).desc()) if order_direction == 'desc' else queryset.order_by(Lower(order_by))
            elif order_by == 'rank':
                queryset = sorted(queryset, key=lambda i: i.rank(), reverse=True) if order_direction == 'desc' else sorted(queryset, key=lambda i: i.rank())
            else:
                if order_direction == 'desc':
                    order_by = '-' + order_by
                queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(MySong, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', None)
        context['direction'] = self.request.GET.get('direction', None)
        context['PROJECT_URI'] = settings.PROJECT_URI
        return context



class DeactiveSong(LoginRequiredMixin,View):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'
    success_message = None
    def get(self, request):
        pkid = request.GET['pk']
        SongObj = get_object_or_404(Song, pk=pkid, user=request.user)

        if SongObj:
            SongObj.active=False
            SongObj.save()

        return HttpResponse(200)


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'email_templates/plain/reset_password.html'
    extra_email_context = { 'PROJECT_URI': settings.PROJECT_URI }
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = 'email_templates/html/reset_password.html'
    subject_template_name = 'email_templates/plain/reset_password.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Reset Your Password')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.extra_email_context['receiver_email'] = self.request.POST.get('email', '')
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return HttpResponse(200)


class HideSong(LoginRequiredMixin, View):
    login_url = settings.REDIRECT_URL
    redirect_field_name = 'next'
    success_message = None

    def post(self, request):
        pkid = request.POST.get('pk')
        hidden = request.POST.get('hidden', None)
        SongObj = get_object_or_404(Song, pk=pkid, user=request.user)

        if SongObj:
            SongObj.hidden = True if hidden == 'true' else False
            SongObj.save()

        return HttpResponse(200)


def upload_song_for_analysis(song,request):

    if settings.USE_AWS:
        url = song.file.url
    else:
        url = "".join((settings.PROJECT_URI, song.file.url))

    deas_id = None

    try:
        result = post_song_from_url(url)
        deas_id = result.get('data', {}).get('id', None)

        if not deas_id:
            db_logger.new_logger(request, type="errors", description="[apps.accounts.views.upload_song_for_analysis] Could not upload song ({}) for analysis: {}".format(url, result))
            logger.error("[apps.accounts.views.upload_song_for_analysis] Could not upload song ({}) for analysis: {}".format(url, result))
    except Exception as e:
        db_logger.new_logger(request, type="errors", description="[apps.accounts.views.upload_song_for_analysis] Could not upload song ({}) for analysis: {}".format(url, e))
        logger.error("[apps.accounts.views.upload_song_for_analysis] Could not upload song ({}) for analysis: {}".format(url, e))
    return deas_id


def add_to_newsletter(request):
    courriel = request.GET['email']
    result = add_subscribers(courriel)
    return HttpResponse(status=200, content=result)


def getpartnerinfo (partner):
    partner_info = {}

    if partner.is_partner:
        totalcredit, totalcash, totalsongs, totalvisits = (False,) * 4
        users = partner.referee.values()

        for usr in users:
            usersongs = Song.objects.filter(user=usr['id'])
            totalsongs += len(usersongs)

        partner_info = {
            'totaluploads': totalsongs,
            'user': partner
        }


    return partner_info


class PartnerDashboard(LoginRequiredMixin, View):
    # template = 'pages/myAccount/myAccountStats.html'
    template = 'pages/myAccount/myAccountPartnerStats.html'
    def get(self, request):
        if not request.user.is_partner or not request.user.approved_partner:
            db_logger.new_logger(request, type="errors", description=_("Try to get in partner dashboard without right"))
            return redirect('home')

        SongUpload = Song.objects.filter(user__pk__in=list(CustomUser.objects.filter(referrer=request.user).values_list('pk', flat=True))).count()
        return render(request, self.template, {'totalSongUpload':SongUpload, 'link':'https://deas.hitlab.com/?ref='})

    def post(self, request):
        # Vérification de l'authentification et de l'existance du User comme Partenair
        try:
            if not request.user.is_partner or not request.user.approved_partner:
                db_logger.new_logger(request, type="errors", description=_("Try to make partner request without right"))
                return JsonResponse({'errors': 'Partner Errors'}, status=401)
        except:
            db_logger.new_logger(request, type="errors", description=_("Partner Errors"))
            return JsonResponse({'errors': 'Partner Errors'}, status=401)

        if request.is_ajax():
            code_form = CheckPartnerCodeForm(request.POST, user=request.user)
            if code_form.is_valid():
                request.user.referral_code = code_form.cleaned_data['referral_code']
                request.user.save()
                return JsonResponse({'saved': 1}, status=200)
            else:
                db_logger.new_logger(request, type="errors", description=code_form.errors)
                return JsonResponse({'errors': code_form.errors}, status=401)
        else:
            db_logger.new_logger(request, type="errors", description=_("Only ajax request needed."))


@require_POST
def checkpartnercode(request):
    #Vérification de l'authentification et de l'existance du User comme Partenair
    try:
        if not request.user.is_partner or not request.user.approved_partner:
            db_logger.new_logger(request, type="errors", description=_("Try to make partner request without right"))
            return JsonResponse({'errors': 'Partner Errors'}, status=401)
    except:
        db_logger.new_logger(request, type="errors", description=_("Try to make partner request without right"))
        return JsonResponse({'errors': 'Partner Errors'}, status=401)

    if request.method == 'POST' and request.is_ajax():
        code_form = CheckPartnerCodeForm(request.POST, user=request.user)
        if code_form.is_valid():
            exist_code = CustomUser.objects.filter(Q(referral_code = code_form.cleaned_data['referral_code']) & ~Q(pk = request.user.pk) )
            if len(exist_code) > 0 :
                return JsonResponse({'exist_code': 1}, status=200)
            return JsonResponse({'exist_code': 0}, status=200)
        else:
            db_logger.new_logger(request, type="errors", description=code_form.errors)
            return JsonResponse({'errors': code_form.errors}, status=401)


@require_POST
def edit_user_address(request):
    data = json.loads(request.POST.get('data', ''))
    if data:
        billing_details = data.get('billing_details', None)
        if billing_details:
            try:
                request.user.address = billing_details.get("address", {}).get("line1", None)
                request.user.city = billing_details.get("address", {}).get("city", None)
                request.user.state = billing_details.get("address", {}).get("state", None)
                request.user.country = billing_details.get("address", {}).get("country", None)
                request.user.zip = billing_details.get("address", {}).get("postal_code", None)
                request.user.save()
            except Exception as e:
                db_logger.new_logger(request, type="errors", description="[apps.accounts.views.edit_user_address] Could not modify user address: {}".format(e))
                logger.error("[apps.accounts.views.edit_user_address] Could not modify user address: {}".format(e))

    return JsonResponse({})


def autocompletePartner(request):
    if request.is_ajax() and request.user.is_authenticated and request.user.is_superuser:
        query = request.GET.get("term", "")
        listpartner = CustomUser.objects.filter(email__icontains=query, approved_partner=True, is_partner=True)[:10]

        results = []
        for partner in listpartner:
            results.append({'value': partner.email, 'data': partner.email})

        data = json.dumps(results)
        mimetype = "application/json"
        return HttpResponse(data, mimetype)


class ChangeAddress(LoginRequiredMixin, FormView):
    template = 'modules/_changeAddressForm.html'

    def get(self, request):
        address_form = AddressChangeForm(instance=request.user)
        return render(request, self.template, {'profile_form': address_form})

    def post(self, request):
        address_form = AddressChangeForm(instance=request.user, data=request.POST)
        status_code = 200
        if address_form.is_valid():
            address_form.save()
        else:
            db_logger.new_logger(request, type="errors", description=_('Update Address Operation failure !'))
            status_code = 400

        return render(request, self.template, {'address_form': address_form}, status=status_code)
