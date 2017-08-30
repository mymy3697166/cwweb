$(function() {
  $("#content").css("min-height", $("body").height() - 100);
});

var siteApp = angular.module("siteApp", []);

siteApp.controller("TagCtrl", ["$scope", "$http", function($scope, $http) {
  $scope.params = {page: 0, rows: 15};

  $scope.list = [];
  $scope.fetch = function() {
    $http.post('/tag/fetch', $scope.params).then(function(e) {
      $scope.list = e.data.data;
    });
  };

  $scope.fetch();
}]);