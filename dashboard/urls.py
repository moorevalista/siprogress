from django.urls import re_path
from django.urls import include, path

from dashboard import privelige
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    # edit juan start
    url(r"divisi/",
        include(
            [
                url(r"^$", views.divisi, name="divisi"),
                url(r"^getDivisi", views.getDivisi, name="getDivisi"),
                url(r"^getIdDivisi", views.getIdDivisi, name="getIdDivisi"),
                url(r"^saveDivisi", views.saveDivisi, name="saveDivisi"),
                url(r"^deleteDivisi", views.deleteDivisi, name="deleteDivisi"),
            ]
        )),
    url(r"komplain/",
        include(
            [
                url(r"^$", views.komplain, name="komplain"),
                url(r"^getKomplain", views.getKomplain, name="getKomplain"),
                url(r"^getIdKomplain", views.getIdKomplain, name="getIdKomplain"),
                url(r"^saveKomplain", views.saveKomplain, name="saveKomplain"),
                url(r"^deleteKomplain", views.deleteKomplain, name="deleteKomplain"),
                url(r"^updateStatus", views.updateStatus, name="updateStatus"),
                # url(r"^listAllKomplain", views.listAllKomplain, name="listAllKomplain"),
            ]
        )),
    url(
        r"^listAduan/",
        include(
            [
                url(r"^$", views.listAllKomplain, name="listAllKomplain"),
                url(r"^aduan/",
                    include(
                        [
                            url(r"^get", views.get_list_aduan, name="get_list_aduan"),
                            url(r"^update", views.get_list_aduan, name="get_list_aduan"),
                            url(r"^deleteAduan", views.deleteAduan, name="deleteAduan"),
                        ]
                    ),
                ),
            ]
        ),
    ),

    # edit juan end
    url(
        r"^privilege/",
        include(
            [
                url(r"^$", privelige.dashboard, name="privilege"),
                url(r"^menu/", privelige.menu, name="menu"),
                url(r"^menu_priv/", privelige.menu_priv, name="menu_priv"),
                url(r"^menu_post", privelige.menu_post, name="menu_post"),
                url(r"^user/", privelige.user, name="user"),
                url(r"^navbars/", privelige.navbars, name="navbars"),
                url(r"^navbars_priv/", privelige.navbars_priv, name="navbars_priv"),
                url(r"^navbars_post", privelige.navbars_post, name="navbars_post"),
                url(
                    r"^subnavbars_priv/",
                    privelige.subnavbars_priv,
                    name="subnavbars_priv",
                ),
                url(
                    r"^subnavbars_post",
                    privelige.subnavbars_post,
                    name="subnavbars_post",
                ),
                url(r"^menubars/", privelige.menubars, name="menubars"),
                url(r"^menubars_priv/", privelige.menubars_priv, name="menubars_priv"),
                url(
                    r"^submenubars_priv/",
                    privelige.submenubars_priv,
                    name="submenubars_priv",
                ),
                url(r"^menubars_post", privelige.menubars_post, name="menubars_post"),
                url(
                    r"^submenubars_post",
                    privelige.submenubars_post,
                    name="submenubars_post",
                ),
            ]
        ),
    ),
]