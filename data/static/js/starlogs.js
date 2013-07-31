(function() {
    var self = this;
    $(function() {
        var animationEnd, transitionEnd, crawl, playCommits, playError, url;
        animationEnd = "animationend webkitAnimationEnd MSAnimationEnd oAnimationEnd";
        transitionEnd = "webkitTransitionEnd transitionend msTransitionEnd oTransitionEnd";

        crawl = function(messages) {
            var counter, delay;
            counter = 0;
            delay = function() {
                var lastMessageDivHeight;
                lastMessageDivHeight = $(".content:last").height();
                return 1e3 + 500 * lastMessageDivHeight / 18;
            };
            if (messages.length > 0) {
                $(".plane").append($("<div>", {
                    "class": "content"
                }).text(messages[0]));
                setTimeout(function() {
                    return crawl(messages.slice(counter));
                }, delay());
                return ++counter;
            } else {
                return counter = 0;
            }
        };
        playCommits = function(commits) {
            document.getElementById("theme").play();
            var messages = [];
            for (var i = 0; i < commits.length; i++) {
                messages.push(commits[i].desc);
            }
            return crawl(messages);
        };

        playError = function() {
            document.getElementById("imperial_march").play();
            return crawl([ "Tun dun dun, da da dun, da da dun ...", "Couldn't find the repo, the repo!" ]);
        };

        $(document).on(animationEnd, ".content", function() {
            return $(this).remove();
        });

        loadRepository = function (url) {
            $.ajax(url + '/jsonp_log', {
                'dataType': 'jsonp',
                'success': playCommits,
                'error': playError
            });
        };
    });
}).call(this);
