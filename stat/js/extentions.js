$(document).ready(function(){
    function page_alert()
    {
    old_text = $('.tagline').text();
    //alert(old_text);
    $('.tagline').addClass('tagline-error');
    $('.tagline').text('Дважды голосовать за один статус НЕЛЬЗЯ!!!');
    setTimeout(function() {
                $('.tagline').removeClass('tagline-error');
                $('.tagline').text(old_text);
            }, 3000);
        }
    $('.new').click(function(){
        indd = $(this).text();
        if ($(this).hasClass('resolved'))
            {page_alert()}
        else
            {$.get($(this).attr('href'));
             $(this).text(parseInt(indd)+1);
             $(this).removeClass('new');
             $(this).addClass('resolved');
            }
        return false;
        })
    $('.critical').click(function(){
        indd = $(this).text();
        if ($(this).hasClass('resolved'))
            {page_alert()}
        else
        {
            $.get($(this).attr('href'));
            $(this).text(parseInt(indd)-1);
            $(this).removeClass('critical');
            $(this).addClass('resolved');
        }
            return false;
        })

$('.ticket').click(function(){
            $(this).find('.ticket-meta').slideToggle("fast")
        },
        function(){
            $(this).find('.ticket-meta').slideToggle("fast")
        });
});

