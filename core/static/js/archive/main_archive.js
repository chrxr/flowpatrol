(function(){
    var itemContainer = $(".itemContainer"), 
        imageCount = itemContainer.length - 1,
        innerContainer = $(".innerContainer")[0],
        button = $("#button"),
        containerHeight = imageCount * 480;
        console.log(itemContainer);
    for (i = 0; i <= imageCount; ++i) {
        var indItem = $(itemContainer)[i];
        $(indItem).addClass("pic-" + i);
    };
    $(button).click(function(){nextImage()});
    $(innerContainer).css({height: containerHeight});

    function nextImage() {
        $(innerContainer).css({top:'480px'});
    }
})()

