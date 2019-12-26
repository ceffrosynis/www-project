from django.shortcuts import render, redirect
from .forms import UserProfileForm, SearchForm
from .models import User, BTCWallet, ETHWallet, LTCWallet
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .walletapi import *
from django.contrib.auth import get_user_model

# Create your views here.

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

class profile(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(UserID=request.user)
        if user.exists():
            btc = BTCWallet.objects.filter(UserID=request.user)
            if not btc.exists():
                btc=''
            else:
                btc=btc[0].BTC
            eth = ETHWallet.objects.filter(UserID=request.user)
            if not eth.exists():
                eth=''
            else:
                eth=eth[0].ETH
            ltc = LTCWallet.objects.filter(UserID=request.user)
            if not ltc.exists():
                ltc=''
            else:
                ltc=ltc[0].LTC
            try:
                if request.GET['newbtc']:
                    btc = BTCWallet.objects.filter(UserID=request.user)
                    if btc.exists():
                        btc.delete()
                    btc = CreateBTCWallet()
                    b=BTCWallet.create(request.user, btc)
            except:
                pass
            form = UserProfileForm(initial={
                'FirstName': user[0].FirstName,
                'LastName': user[0].LastName,
                'Email': user[0].Email,
                'BTC': btc,
                'ETH': eth,
                'LTC': ltc
            })
            context = {
                'form': form
            }
            return render(request, 'profile.html', context=context)
        form = UserProfileForm(self.request.POST or None)
        return render(request, 'profile.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(self.request.POST or None)
        if form.is_valid():
            FirstName = form.cleaned_data.get('FirstName')
            LastName = form.cleaned_data.get('LastName')
            Email = form.cleaned_data.get('Email')
            BTCField = form.cleaned_data.get('BTC')
            ETHField = form.cleaned_data.get('ETH')
            LTCField = form.cleaned_data.get('LTC')
            user = User.objects.filter(UserID=request.user)
            if user.exists():
                UserProfile=user[0]
                UserProfile.FirstName=FirstName
                UserProfile.LastName=LastName
                UserProfile.Email=Email
                UserProfile.save()
            else:
                User.objects.create(UserID=request.user, FirstName=FirstName, LastName=LastName, Email=Email)
            btc = BTCWallet.objects.filter(UserID=request.user)
            if btc.exists():
                BTC=btc[0]
                BTC.BTC = BTCField
                if BTCField == '':
                    btc.delete()
                else:
                    BTC.save()
            else:
                if BTCField != '':
                    BTCWallet.objects.create(UserID=request.user, BTC=BTCField)
            
            eth = ETHWallet.objects.filter(UserID=request.user)
            if eth.exists():
                ETH=eth[0]
                ETH.ETH = ETHField
                if ETHField == '':
                    eth.delete()
                else:
                    ETH.save()
            else:
                if ETHField != '':
                    ETHWallet.objects.create(UserID=request.user, ETH=ETHField)
        
            ltc = LTCWallet.objects.filter(UserID=request.user)
            if ltc.exists():
                LTC=ltc[0]
                LTC.LTC = LTCField
                if LTCField == '':
                    ltc.delete()
                else:
                    LTC.save()
            else:
                if LTCField != '':
                    LTCWallet.objects.create(UserID=request.user, LTC=LTCField)

        return render(request, 'profile.html', context={'form': form})


class index(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(UserID=request.user)
        form = SearchForm()
        if user.exists():
            btc = BTCWallet.objects.filter(UserID=request.user)
            
            eth = ETHWallet.objects.filter(UserID=request.user)

            ltc = LTCWallet.objects.filter(UserID=request.user)

            btc_img=''
            eth_img=''
            ltc_img=''

            if btc.exists():
                btc_img=GenerateImage(btc[0].BTC, "bitcoin")
            if eth.exists():
                eth_img=GenerateImage(eth[0].ETH, "ethereum")
            if ltc.exists():
                ltc_img=GenerateImage(ltc[0].LTC, "litecoin")
            
            context = {
                'btc': btc,
                'eth': eth,
                'ltc': ltc,
                'btc_img': btc_img,
                'eth_img': eth_img,
                'ltc_img': ltc_img,
                'form': form
            }
            return render(request, 'index.html', context=context)

        return redirect('crypto:profile')

    def post(self, request, *args, **kwargs):
        UserModel = get_user_model()
        context = {}
        form = SearchForm(self.request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('search')
            user = UserModel.objects.filter(username__contains=username)
            if user.exists():
                
                user = User.objects.filter(UserID__in=user)
        
                context = {
                    'user': user
                }

        return render(request, 'search.html', context=context)
    

class List(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pass
        
    def post(self, request, *args, **kwargs):
        pass