<<<<<<< HEAD
function addToCart(productid){
=======
function addToCart(userid, productid){
>>>>>>> lily-running
    fetch('/add-cart', {
        method:'Post',
        body:JSON.stringify({productid:productid})
    }).then((_res)=> {
      ;
    });
}