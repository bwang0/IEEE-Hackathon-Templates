/*
 * Written by Daeyun Shin for IEEE@UIUC Hackathon. Sept 7, 2012
 */
$(function() {
    function searchTwitter(keyword) {
        $.ajax({
            url: "http://search.twitter.com/search.json",
               dataType: 'jsonp', // allows cross-domain requests
               cache: false,
               data: {
                    q: keyword,
                    rpp: 25 // this is the number of results to return.
                    // read https://dev.twitter.com/docs/api/1/get/search for details
               }
        }).done(function(data) { // this function is called when the ajax request is finished. Variable data contains the returned value.
            var html, name, result, text, _i, _len, results;
            $("#tweets").html(''); // clear html
            results = data["results"];
            for (_i = 0, _len = results.length; _i < _len; _i++) { // iterate through all items in data["results"]. current index is _i
                result = results[_i];
                text = result["text"];
                name = result["from_user"];
                html = ("<div class='tweet'><div class='name'>@" + name + "<span> says:</span></div><div class='text'>" + text + "</div></div>").replace(keyword, "<span>" + keyword + "</span>");
                // the "replace" part adds a <span> tag around the keyword so that css knows which word to highlight
                $("#tweets").append(html); // add the generated html to <div id="tweets"></div>
            }
        });
    };

    $("form").submit(function(e) { // this function is called when the Search button is clicked
        var keyword;
        e.preventDefault(); // we only want to use Javascript to handle the request. so prevent the page from changing
        keyword = $("#keyword").val(); // get the text in the search box
        searchTwitter(keyword); // call the searchTwitter function with the keyword
    });
});
