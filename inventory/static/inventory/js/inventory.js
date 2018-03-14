

    baseApp.controller('subcategoryController',['$scope','$http','toaster','$window',function ($scope,$http,toaster,$window) {
        $scope.product_category;
        $scope.product_subcategory;
        console.log("===================lalalaalaalal===================")
        // console.log(localStorage.getItem('cultSession'));
        //if(!localStorage.getItem('cultSession'))
                // $window.location.href = '/cult_ui/home';
        $scope.getCategory = function () {
             // console.log("========================================")
            console.log("in getCategory",$scope.product_category);
            // $scope.userDetail = JSON.parse(localStorage.getItem('cultSession'));
            var url = '/inventory/get_product/';
            $http({
                url: url,
                method: 'POST',
                data: {
                    "category": $scope.product_category,
                }
            })
                .then(function (response) {
                    console.log("------safkjalskf----")
                    if (response.data.status === "1")
                        $scope.subcategories = response.data.list;
                        console.log($scope.subcategories);
                }).catch(function (response) {
                    console.log("error");
                })
        }
    }]);


