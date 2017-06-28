function switch_type() {
  var current_type = $( "#market_type :checked" ).val();
  console.log(current_type);

  if (current_type == "buy") {
    $( "#order-submit" ).removeClass("btn-success");
    $( "#order-submit" ).addClass("btn-primary");
    $( "#order-submit" ).val("Place Buy Order");
  } else {
    $( "#order-submit" ).addClass("btn-success");
    $( "#order-submit" ).removeClass("btn-primary");
    $( "#order-submit" ).val("Place Sell Order");
  }
}

$( "#market_type" ).change(switch_type);
