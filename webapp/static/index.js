function addToCart(productid){
    fetch('/add-cart', {
        method:'Post',
        body:JSON.stringify({productid:productid})
    }).then((_res)=> {
      ;
    });
}