function addToCart(userid, productid){
    fetch('/add-cart', {
        method:'Post',
        body:JSON.stringify({ userid:userid, productid:productid})
    }).then((_res)=> {
      ;
    });
}