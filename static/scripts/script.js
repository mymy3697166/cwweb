$(function() {

  $("#content").css("min-height", $("body").height() - 137);
});

function showLoading() {
  var loading = $("<div class='loading'><div class='bg'><img src='/static/images/loading.gif'/><label>加载中...</label></div></div>");
  $("body").append(loading);
}

function hideLoading() {

  $(".loading").remove();
}

function pager(list, total, page, fetch, element) {
  (element || $("#pager")).pagination(total, {
    num_display_entries: 8,
    prev_text: "上一页",
    next_text: "下一页",
    callback: fetch,
    items_per_page: 10,
    current_page: page,
    link_to: "javascript:void(0)"
  });
}

function upload(callback, start) {
  $("#file_iframe").remove();
  var iframe = $("<iframe id='file_iframe' style='display:none;'></iframe>");
  $("body").append(iframe);
  var body = $(iframe[0].contentWindow.document.body);
  var form = $("<form action='/upload' method='post' enctype='multipart/form-data'></form>");
  var file = $("<input type='file' name='file'/>");
  body.append(form.append(file));
  iframe[0].onload = function() {
    var result = $(iframe[0].contentWindow.document.body).html();
    if(callback) callback($.parseJSON(result));
  };
  file.click();
  file.change(function() {
    form.submit();
    if (start) start();
  });
}

var siteApp = angular.module("siteApp", []);

siteApp.controller("TagCtrl", ["$scope", "$http", function($scope, $http) {
  // 定义数据
  $scope.params = {page: 0, rows: 10, sstatus: 0};
  $scope.list = [];
  // 定义函数
  $scope.fetch = function(page) {
    $scope.params.page = page || 0;
    showLoading();
    $http.post('/tag/fetch', $scope.params).then(function(e) {
      hideLoading();
      $scope.list = e.data.data;
      pager($scope.list, e.data.count, page, $scope.fetch);
    });
  };
  $scope.update = function(data) {
    showLoading();
    $http.post('/tag/update', _.extend(data, $scope.params)).then(function(e) {
      hideLoading();
      $scope.list = e.data.data;
      pager($scope.list, e.data.count, $scope.params.page, $scope.fetch);
      $("#editor").modal("hide");
    });
  };
  $scope.show_edit_status = function(item) {
    if (confirm("确定要" + (item.status == 0 ? "弃用" : "启用") + "该记录吗？")) {
      $scope.update({id: item.id, status: item.status == 0 ? 1 : 0});
    }
  };
  $scope.show_edit = function(item) {
    $scope.edit_item = {};
    if (item) $scope.edit_item = {id: item.id, name: item.name, cover: item.cover, description: item.description, tag: item.tag};
    $("#editor").modal("show");
  };
  $scope.upload = function() {
    upload(function(e) {
      $scope.$apply(function() {
        $("#btn_upload").button("reset");
        $scope.edit_item.cover = {id: e.id, origin_url: e.url};
      });
    }, function() {$("#btn_upload").button("loading");});
  };
  $scope.input_all = function() {
    return  $scope.edit_item &&
      $scope.edit_item.name &&
      $scope.edit_item.name != "" &&
      $scope.edit_item.cover &&
      $scope.edit_item.cover.id &&
      $scope.edit_item.cover.id != ""
  };
  // 初始化
  $("#editor").on("hidden.bs.modal", function() {
    $scope.edit_item = {};
  });
  $http.post("/tag/fetch_tags").then(function(e) {
    $scope.tags = e.data.data;
  });
  $scope.fetch();
}]);

siteApp.controller("WallpaperCtrl", ["$scope", "$http", function($scope, $http) {
  // 定义数据
  $scope.params = {page: 0, rows: 10, sstatus: 0};
  $scope.list = [];
  // 定义函数
  $scope.fetch = function(page) {
    $scope.params.page = page || 0;
    showLoading();
    $http.post('/wallpaper/fetch', $scope.params).then(function(e) {
      hideLoading();
      $scope.list = e.data.data;
      pager($scope.list, e.data.count, page, $scope.fetch);
    });
  };
  $scope.update = function(data) {
    showLoading();
    $http.post('/wallpaper/update', _.extend(data, $scope.params)).then(function(e) {
      hideLoading();
      $scope.list = e.data.data;
      pager($scope.list, e.data.count, $scope.params.page, $scope.fetch);
      $("#editor").modal("hide");
    });
  };
  $scope.show_edit_status = function(item) {
    if (confirm("确定要" + (item.status == 0 ? "弃用" : "启用") + "该记录吗？")) {
      $scope.update({id: item.id, status: item.status == 0 ? 1 : 0});
    }
  };
  $scope.show_edit = function(item) {
    $scope.edit_item = {};
    $scope.tags.forEach(function(tag) {
      delete tag.checked;
    });
    if (item) {
      $scope.tags.forEach(function(atag) {
        if (_.findIndex(item.tags, function(tag) {return atag.id == tag.id;}) >= 0)
          atag.checked = true;
      });
      $scope.edit_item = {id: item.id, name: item.name, image: item.image, price: item.price, tags: item.tags, user: item.user};
    }
    $("#editor").modal("show");
  };
  $scope.upload = function() {
    upload(function(e) {
      $scope.$apply(function() {
        $("#btn_upload").button("reset");
        $scope.edit_item.image = {id: e.id, origin_url: e.url};
      });
    }, function() {$("#btn_upload").button("loading");});
  };
  $scope.input_all = function() {
    return  $scope.edit_item &&
      $scope.edit_item.name &&
      $scope.edit_item.name != "" &&
      $scope.edit_item.image &&
      $scope.edit_item.image.id &&
      $scope.edit_item.image.id != "" &&
      $scope.edit_item.tags &&
      $scope.edit_item.tags.length > 0 &&
      $scope.edit_item.user &&
      $scope.edit_item.user.id &&
      $scope.edit_item.user.id != "" &&
      $scope.edit_item.price != undefined
  };
  $scope.tag_checked = function() {

    $scope.edit_item.tags = _.filter($scope.tags, function(item) {return item.checked;});
  };
  $scope.tag_filter = function(tag) {
    return _.filter($scope.tags, function(item) {
      return tag == item.tag;
    });
  };
  $scope.toggle_tags = function(evt, index) {
    $(".tag-children").each(function(i) {
      if (index == i) $(this).toggle();
      else $(this).hide();
    });
  };
  // 初始化
  $("#editor").on("hidden.bs.modal", function() {
    $scope.edit_item = {};
  });
  $http.post("/wallpaper/fetch_tags").then(function(e) {
    $scope.tags = e.data.data;
  });
  $http.post("/user/fetch_default").then(function(e) {
    $scope.users = e.data.data;
  });
  $scope.fetch();
}]);

siteApp.controller("ThemeCtrl", ["$scope", "$http", function($scope, $http) {
  // 定义数据
  $scope.params = {page: 0, rows: 10, sstatus: 0};
  $scope.wps_params = {page: 0, rows: 10};
  $scope.search_params = {key: "", page: 0, rows: 10};
  $scope.list = [];
  $scope.swps = [];
  // 定义函数
  $scope.fetch = function(page) {
    $scope.params.page = page || 0;
    showLoading();
    $http.post('/theme/fetch', $scope.params).then(function(e) {
      hideLoading();
      $scope.list = e.data.data;
      pager($scope.list, e.data.count, page, $scope.fetch);
    });
  };
  $scope.fetch_wps = function(page) {
    $scope.wps_params.page = page || 0;
    $scope.wps_params.id = $scope.edit_item.id;
    showLoading();
    $http.post('/theme/fetch_wps', $scope.wps_params).then(function(e) {
      hideLoading();
      $scope.wps = e.data.data;
      pager($scope.wps, e.data.count, $scope.wps_params.page, $scope.fetch_wps, $("#wps-pager"));
    });
  };
  $scope.search_wps = function(next) {
    if (next == undefined) $scope.search_params.page = 0;
    if (next == true) $scope.search_params.page++;
    if (next == false) $scope.search_params.page--;
    showLoading();
    $http.post('/theme/search_wps', $scope.search_params).then(function(e) {
      hideLoading();
      $scope.swps_page_count = Math.ceil(e.data.count / $scope.search_params.rows) - 1;
      $scope.swps = e.data.data;
    });
  };
  $scope.update = function(data) {
    showLoading();
    $http.post('/theme/update', _.extend(data, $scope.params)).then(function(e) {
      hideLoading();
      $scope.list = e.data.data;
      pager($scope.list, e.data.count, $scope.params.page, $scope.fetch);
      $("#editor").modal("hide");
    });
  };
  $scope.show_edit_status = function(item) {
    if (confirm("确定要" + (item.status == 0 ? "弃用" : "启用") + "该记录吗？")) {
      $scope.update({id: item.id, status: item.status == 0 ? 1 : 0});
    }
  };
  $scope.show_edit = function(item) {
    $scope.edit_item = {};
    if (item) $scope.edit_item = {id: item.id, name: item.name, cover: item.cover, description: item.description, user: item.user};
    $("#editor").modal("show");
  };
  $scope.show_wps = function(item) {
    $scope.edit_item = item;
    $scope.fetch_wps();
    $("#wps").modal("show");
    $scope.search_wps();
  };
  $scope.remove_wp = function(item) {
    if (confirm("确定要移除该壁纸吗？")) {
      showLoading();
      $http.post('/theme/remove_wp', _.extend({twp_id: item.id}, $scope.wps_params)).then(function(e) {
        hideLoading();
        $scope.wps = e.data.data;
        pager($scope.wps, e.data.count, $scope.wps_params.page, $scope.fetch_wps, $("#wps-pager"));
      });
    }
  };
  $scope.add_wp = function(wp) {
    showLoading();
    $http.post('/theme/add_wp', _.extend({theme: $scope.edit_item.id, wallpaper: wp}, $scope.wps_params)).then(function(e) {
      hideLoading();
      if (e.data.status == 1) {
        alert("已加入该主题");
        return;
      }
      $scope.wps = e.data.data;
      pager($scope.wps, e.data.count, $scope.wps_params.page, $scope.fetch_wps, $("#wps-pager"));
    });
  };
  $scope.upload = function() {
    upload(function(e) {
      $scope.$apply(function() {
        $("#btn_upload").button("reset");
        $scope.edit_item.cover = {id: e.id, origin_url: e.url};
      });
    }, function() {$("#btn_upload").button("loading");});
  };
  $scope.input_all = function() {
    return  $scope.edit_item &&
      $scope.edit_item.user &&
      $scope.edit_item.user.id &&
      $scope.edit_item.user.id != "" &&
      $scope.edit_item.name &&
      $scope.edit_item.name != "" &&
      $scope.edit_item.cover &&
      $scope.edit_item.cover.id &&
      $scope.edit_item.cover.id != ""
  };
  // 初始化
  $("#editor").on("hidden.bs.modal", function() {
    $scope.edit_item = {};
  });
  $http.post("/user/fetch_default").then(function(e) {
    $scope.users = e.data.data;
  });
  $scope.fetch();
}]);

siteApp.controller("LoginCtrl", ["$scope", "$http", function($scope, $http) {
  // 定义函数
  $scope.input_all = function() {
    return !$scope.uid || $scope.uid == "" || !$scope.pwd || $scope.pwd == "";
  };
  $scope.login = function(evt) {
    $(evt.target).button("loading");
    $http.post("/login_submit", {uid: $scope.uid, pwd: $scope.pwd}).then(function(e) {
      $(evt.target).button("reset");
      if (e.data.status == 0) {
        location = "/";
      } else {
        alert(e.data.description);
      }
    });
  };
}]);

siteApp.controller("LogoutCtrl", ["$scope", "$http", function($scope, $http) {
  // 定义函数
  $scope.logout = function(evt) {
    $http.post("/logout").then(function(e) {
      location = "/login";
    });
  };
}]);