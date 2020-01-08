from django.shortcuts import render, redirect
from .forms import UserProfileForm, SearchForm, WalletGeneration, VisitProfile
from .models import User, BTCWallet, ETHWallet, LTCWallet
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .walletapi import *
from django.contrib.auth import get_user_model

# Create your views here.

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

class profile(LoginRequiredMixin, View):

    WalletGenerator={'btc': CreateBTCWallet, 'eth': CreateETHWallet, 'ltc': CreateLTCWallet}
    Wallets = {'btc': BTCWallet, 'eth': ETHWallet, 'ltc': LTCWallet}
    arguments = {'btc': {'BTC': None}, 'eth': {'ETH': None}, 'ltc': {'LTC': None}}
    
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(UserID=request.user)
        if user.exists():
            btc, eth, ltc = self.userInfo()

            form = UserProfileForm(initial={
                'FirstName': user[0].FirstName,
                'LastName': user[0].LastName,
                'Email': user[0].Email,
                'BTC': btc,
                'ETH': eth,
                'LTC': ltc
            })

            context = {
                'form': form,
            }
            return render(request, 'profile.html', context=context)
        form = UserProfileForm(self.request.POST or None)
        return render(request, 'profile.html', context={'form': form})

    def userInfo(self):
        btc = BTCWallet.objects.filter(UserID=self.request.user)
        if not btc.exists():
            btc=''
        else:
            btc=btc[0].BTC
        eth = ETHWallet.objects.filter(UserID=self.request.user)
        if not eth.exists():
            eth=''
        else:
            eth=eth[0].ETH
        ltc = LTCWallet.objects.filter(UserID=self.request.user)
        if not ltc.exists():
            ltc=''
        else:
            ltc=ltc[0].LTC

        return (btc, eth, ltc, )


    def post(self, request, *args, **kwargs):
        form = UserProfileForm(self.request.POST or None)
        if form.is_valid():
            if 'WalletGeneration' in request.POST:
                WalletType = request.POST['WalletGeneration']
                print (WalletType)
                if WalletType:
                    wallet = self.Wallets[WalletType].objects.filter(UserID=request.user)
                    if wallet.exists():
                        wallet.delete()
                    wallet = self.WalletGenerator[WalletType]()
                    self.arguments[WalletType][WalletType.upper()] = wallet
                    self.Wallets[WalletType].objects.create(UserID=request.user, **(self.arguments[WalletType]))
                    return redirect('crypto:profile')
        
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

    Wallets = [BTCWallet, ETHWallet, LTCWallet]
    WalletImages = ['', '', '']

    def get(self, request, *args, **kwargs):
        WalletImages = ['', '', '']
        user = User.objects.filter(UserID=request.user)
        form = SearchForm()
        if user.exists():

            WalletIDs = [wallet.objects.filter(UserID=request.user) for wallet in self.Wallets]

            # [WalletID for idx, WalletID in enumerate(WalletIDs) if WalletID.exists()]

            if WalletIDs[0].exists():
                WalletImages[0]=GenerateImage(WalletIDs[0][0].BTC, "bitcoin")
            if WalletIDs[1].exists():
                WalletImages[1]=GenerateImage(WalletIDs[1][0].ETH, "ethereum")
            if WalletIDs[2].exists():
                WalletImages[2]=GenerateImage(WalletIDs[2][0].LTC, "litecoin")
            
            context = {
                'btc': WalletIDs[0],
                'eth': WalletIDs[1],
                'ltc': WalletIDs[2],
                'btc_img': WalletImages[0],
                'eth_img': WalletImages[1],
                'ltc_img': WalletImages[2],
                'form': form
            }
            return render(request, 'index.html', context=context)

        return redirect('crypto:profile')



    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            UserModel = get_user_model()
            button = VisitProfile(self.request.POST or None)
            form = SearchForm()
            if button.is_valid():
                WalletImages = ['', '', '']
                username = button.cleaned_data.get('VisitProfile')
                user = UserModel.objects.filter(username=username)
                
                WalletIDs = [wallet.objects.filter(UserID=user[0]) for wallet in self.Wallets]

                # [WalletID for idx, WalletID in enumerate(WalletIDs) if WalletID.exists()]

                if WalletIDs[0].exists():
                    WalletImages[0]=GenerateImage(WalletIDs[0][0].BTC, "bitcoin")
                if WalletIDs[1].exists():
                    WalletImages[1]=GenerateImage(WalletIDs[1][0].ETH, "ethereum")
                if WalletIDs[2].exists():
                    WalletImages[2]=GenerateImage(WalletIDs[2][0].LTC, "litecoin")
                
                context = {
                    'btc': WalletIDs[0],
                    'eth': WalletIDs[1],
                    'ltc': WalletIDs[2],
                    'btc_img': WalletImages[0],
                    'eth_img': WalletImages[1],
                    'ltc_img': WalletImages[2],
                    'form': form,
                    'username': username
                }
                return render(request, 'index.html', context=context)

            context = {}
            form = SearchForm(self.request.POST or None)
            if form.is_valid():
                username = form.cleaned_data.get('search')
                user = UserModel.objects.filter(username__contains=username)
                if user.exists():
                    user = User.objects.filter(UserID__in=user)
                    context = {
                        'user': user,
                        'form': form
                    }

            return render(request, 'search.html', context=context)
        return redirect('crypto:index')