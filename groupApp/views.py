import json
from .models import Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.gis import serializers
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from UserApp.models import CustomizedUser
from groupApp.forms import CreateGroupForm

from dal import autocomplete

from groupApp.models import Group


@login_required
def create_group(request):
    if request.method == 'POST':
        create_form = CreateGroupForm(request.POST)

        if create_form.is_valid():
            admin = request.user
            # if admin not in create_form.cleaned_data['member']:
            #     print()

            create_form_obj = create_form.save(commit=False)
            create_form_obj.admin = admin
            create_form_obj.save()
            create_form.save_m2m()

        return render(request, 'CreateGroup.html', {'create_form': CreateGroupForm(), 'create': True})

    else:
        create_form = CreateGroupForm(initial={'title': '', 'member': [request.user]})
        return render(request, 'CreateGroup.html', {'create_form': create_form, 'create': True})


class MembersAutoComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = CustomizedUser.objects.all()
        if self.q:
            qs = qs.filter(Q(email__contains=self.q))
        return qs


@login_required
def groups_list(request):
    if request.method == 'GET':
        admin_is_not_member = False

        groups = Group.objects.filter(Q(admin=request.user)|Q(member=request.user)).distinct()
        for group in groups:
            print(group.title, group.member.all())
            # if admin not in group.member.all():
            #     print(admin, 'not in ', group.member.all(), 'group name: ', group)
            #     group.owner = admin
            # if group.admin == request.user:
            #     group.owner = True

            if group.admin == request.user and group.admin not in group.member.all():
                print(request.user not in group.member.all())
                admin_is_not_member = True
        print(groups)
        return render(request, 'CreateGroup.html', {'groups_list': True, 'groups': groups,
                                                    'admin_is_not_member': admin_is_not_member})
    else:
        pass


@login_required
def edit_group(request, id):

    if request.method == 'GET':
        group = Group.objects.get(id=id)
        if not group.admin == request.user:
            return render(request, 'CreateGroup.html', {'message': 'شما اجازه دسترسی به این بخش را ندارید.'})
        edit_group_form = CreateGroupForm(instance=group)

        return render(request, 'CreateGroup.html', {'edit_group_form': edit_group_form, 'edit_group': True})

    elif request.method == 'POST':
        instance = get_object_or_404(Group, id=id)
        edit_group_form = CreateGroupForm(request.POST, instance=instance)

        if edit_group_form.is_valid():
            edit_group_form.save()
        return redirect(reverse('groups-list'))

    return redirect(reverse('groups-list'))


@login_required
def get_members(request, id):
    group = Group.objects.filter(id=id)

    # members = CustomizedUser.objects.filter(group__in=group)
    members = CustomizedUser.objects.filter(group_member__in=group)
    # print(group.all())
    a = serializers.serialize('json', members)
    return HttpResponse(a, content_type='application/json')
