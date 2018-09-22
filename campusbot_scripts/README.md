1. get_data.py
* What does it do?
It uses the courses.json file to fetch data about each course and fill student.json. Optionally you can store the individual csv files for each course.
Hint: Take a look at courses.json and then student.json in sample_database. The cs files for each course are present inside the folder csv_files

* How to call?
```
python3 get_data.py --writecsv <path_to_database>
```

2. events.js
* What does it do? 
This one is used to fetch data about all fb events. It exports two functions, story and get_events. The story function was never used. And the get_events functions accepts a callback function with one parameter for results

* How to call?
This is how it gets called in main bot.js
events.get_events(function(result){
            var attach = [];
            result.forEach(function(ev){
                var card = new builder.ThumbnailCard(session)
                            .title(ev.name)
                            .subtitle(ev.start_time+" - "+ev.end_time)
                            .tap(
                                builder.CardAction.openUrl(session,ev.link)
                            );
                if(ev.cover){
                    card = card.images([builder.CardImage.create(session,ev.cover)]);
                }
                attach.push(card);
            });
            var msg = new builder.Message(session)
                    .attachmentLayout(builder.AttachmentLayout.carousel)
                    .attachments(attach);
            session.endDialog(msg);
        });