'use strict';
 var baseApp = angular.module('baseInvApp', ['ngCookies', 'ngStorage', 'toaster'])
    .config(['$interpolateProvider', function($interpolateProvider) {
        $interpolateProvider.startSymbol('{(');
        $interpolateProvider.endSymbol(')}');
    }])

    baseApp.controller('baseController',['$scope','$http','toaster','$window',function ($scope,$http,toaster,$window) {
            console.log("==-=-=-=========================")
            console.log("==-=-=-=========================")
        $scope.supplier;
        $scope.p_id;
        $scope.customer;
        $scope.total
            console.log("==-=-=-=========================")
        $scope.getProduct = function(){
                console.log("==-=-=-===================0000000000======")
            console.log("in getProduct",$scope.supplier);
            var url = '/inventory/get_purchase/';
            $http({
                url: url,
                method: 'POST',
                data: {
                    "supplier": $scope.supplier,
                    "total": $scope.total,
                }
            })
                .then(function (response) {
                    console.log("------safkjal--------skf----")
                    if (response.data.status === "1") {
                        $scope.products = response.data.list;
                    }
                        console.log($scope.products);
                }).catch(function (response) {
                    console.log("error");
                })
        }

        $scope.getDiscount = function () {
            console.log("==-=-=-===555555555======================")
            console.log("in getDiscount",$scope.customer);
            var url = '/inventory/get_discount/';
            $http({
                url: url,
                method: 'POST',
                data: {
                    "customer": $scope.customer,
                }
            })
                .then(function (response) {
                    console.log("------safk000000000000jal--------skf----")
                    if (response.data.status === "1") {
                        $scope.discount = response.data.list;
                        console.log($scope.discount);

                    }
                        console.log($scope.products);
                }).catch(function (response) {
                    console.log("error");
                })
        }

    }])