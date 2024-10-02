Test Assignment - Backend @Pure

Finally, the day has arrived - you have joined Pure App! Your first task is to create a simple
Django application.

The main goal of this application is to store data for the special chats which will be used to
communicate with users: send them personal promotions and announcements. Each user has
one chat, and every chat can contain a lot of messages. Each message is personal: different
users could get different messages, but we also can send the same message for all users.

Firstly, you will need to create models of the chats and messages. Please store the user UUID,
the date of chat’s creation, the text of the message and the date of message’s creation. Also,
the marketing team sometimes wants to send photos and memes, so please find a place in your
models to store image files. Implement an admin panel to manage these entities.

The first feature of this project will be sending banners from an external API. The performance
team created the API with the list of images which we need to show to users when we want to
increase retention. The API is placed here, and the full documentation is here. Create an
interface in the admin panel which allows sending a message with one photo from this API to all
chats. Take the first image, which we haven’t sent yet, from the URL field. Show the error if
there is no photo to send or any other problems with the API. The production web server before
our application has a 30 seconds timeout for requests, so the admin interface should respond
quickly.

The application should be possible to run using the docker-compose. Please write a short
description on how to run it and how to run the tests. You can use any additional libraries, tools
and databases if they are inside the docker compose configuration. Push results to
GitHub/GitLab/Bitbucket and provide a link.



<h1>The server will be available on localhost:80</h1>
