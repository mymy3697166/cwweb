$(function() {
  $("#content").css("min-height", $("body").height() - 100);
});

function showLoading() {
  var loading = $("<div class='loading'><div class='bg'><img src='/static/images/loading.gif'/><label>加载中...</label></div></div>");
  $("body").append(loading);
}

function hideLoading() {

  $(".loading").remove();
}

function pager(list, total, page, fetch) {
  $("#pager").pagination(total, {
    num_display_entries: 8,
    prev_text: "上一页",
    next_text: "下一页",
    callback: fetch,
    items_per_page: 15,
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
  $scope.params = {page: 0, rows: 15, sstatus: 0};
  $scope.list = [];

  $scope.fetch = function(page) {
    $scope.params.page = page || 0;
    showLoading();
    $http.post('/tag/fetch', $scope.params).then(function(e) {
      hideLoading();
      $scope.list = e.data.data;
      pager($scope.list, e.data.count, page, $scope.fetch)
    });
  };
  $scope.update = function(data) {
    showLoading();
    $http.post('/tag/update', _.extend($scope.params, data)).then(function(e) {
      hideLoading();
      $scope.list = e.data.data;
      pager($scope.list, e.data.count, $scope.params.page, $scope.fetch)
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
  $http.post("/tag/fetch_tags").then(function(e) {
    $scope.tags = e.data.data;
  });
  $scope.fetch();
}]);