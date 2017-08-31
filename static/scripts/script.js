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
    $http.post('/tag/update', data).then(function(e) {
      hideLoading();
      $scope.list = e.data.data;
      pager($scope.list, e.data.count, $scope.params.page, $scope.fetch)
    });
  };
  $scope.show_edit = function(item) {
    if (confirm("确定要删除该记录吗？")) {
      update(_.extend($scope.params, {id: item.id, status: item.status == 0 ? 1 : 0}));
    }
  };
  $scope.show_edit_status = function(item) {

  };

  $scope.fetch();
}]);