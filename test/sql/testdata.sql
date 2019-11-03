use reminder_app;

-- add users
insert into user values (1,'test', 'testpw', 'test@kent.edu');

-- add notes
insert into note (user_id, title, content) values (1,'note1', 'blablabla\nblablabla\nblablabla');
insert into note (user_id, title, content) values (1,'note2', 'blablabla\nblablabla\nblablabla\nblablabla\nblablabla');
insert into note (user_id, title, content) values (1,'note3', 'blablabla\nblablabla');