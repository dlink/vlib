-- vlib tests data creation script

-- May need root to perform these:

-- drop database vlibtests; -- if needed
-- create database vlibtests;
-- grant all on vlibtests.* to vlibtests@localhost identified by 'bogangles';

create table vlibtests.disciplines (
    discipline_id   int(10)         unsigned not null,
    code            varchar(30)     not null,
    name            varchar(45)     not null,
    description     varchar(255)    default null,
    active          int(10)         unsigned not null,
    last_updated    timestamp       not null default current_timestamp on update current_timestamp,
    primary         key             (discipline_id),
    key             state_codes     (code)
)
engine=InnoDB;

insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (0, 'unknown', 'Unknown', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (1, 'accounting', 'Accounting and Tax', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (2, 'biology', 'Biology', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (3, 'business_law', 'Business Law', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (4, 'chemistry', 'Chemistry', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (5, 'communications', 'Communications', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (6, 'economics', 'Economics', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (7, 'english', 'English', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (8, 'finance', 'Finance', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (9, 'business', 'General Business', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (10, 'geosciences', 'Geosciences', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (11, 'information_systems', 'Information Systems', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (12, 'management', 'Management', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (13, 'marketing', 'Marketing', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (14, 'mathematics', 'Mathematics', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (15, 'science', 'Professional and Applied Sciences', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (16, 'psychology', 'Psychology', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (17, 'sociology', 'Sociology', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (18, 'general_business', 'General Business', '', 1);
insert into vlibtests.disciplines (discipline_id, code, name, description, active) values (19, 'alchemy', 'Alchemy', '', 0);

create table vlibtests.books (
  book_id integer unsigned     not null auto_increment primary key,
  book_name varchar(30)        not null,
  title varchar(255)       default null,
  subtitle varchar(255)    default null,
  discipline_id integer unsigned default null,
  num_pages integer unsigned  default 0,
  book_size enum('8.5x11', '6x9') not null default '8.5x11',
  isbn varchar(20)      default null,
  last_updated timestamp       not null 
        default current_timestamp on update current_timestamp,
  created datetime         default null,
  unique key book_name (book_name),
  foreign key (discipline_id)  references disciplines (discipline_id)
) engine InnoDB;
show warnings;

insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('baranoff', 'Risk Management for Enterprises and Individuals', NULL, 8, 771, '8.5x11', '978-0-9823618-0-1', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('bauer', 'Organizational Behavior', NULL, 12, 384, '8.5x11', '978-0-9820430-6-6', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('carpenter', 'Principles of Management', NULL, 12, 412, '8.5x11', '978-0-9820430-7-3', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('collins', 'Exploring Business', NULL, 9, 521, '8.5x11', '978-0-9820430-0-4', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('gallaugher', 'Information Systems', 'A Manager''s Guide to Harnessing Technology', 11, 259, '8.5x11', '978-1-936126-06-4', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('hoyle', 'Financial Accounting', NULL, 1, 457, '8.5x11', '978-0-9823618-3-2', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('lochhaas', 'College Success', NULL, 15, 361, '8.5x11', '978-1-936126-56-9', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('mcafee', 'Introduction to Economic Analysis', NULL, 6, 289, '8.5x11', '978-0-9820430-9-7', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('mccrimmon', 'The Flat World Knowledge Handbook for Writers', NULL, 7, 489, '6x9', '978-1-4533-1073-1', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('mclean', 'Business Communication for Success', NULL, 5, 419, '8.5x11', '978-0-9823618-5-6', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('preston', 'Project Management', 'from Simple to Complex', 11, 242, '8.5x11', '978-0-9823618-8-7', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('preston2', 'Project Management from Simple to Complex', NULL, 11, 241, '8.5x11', '978-1-4533-0268-2', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('price', 'Research Methods in Psychology', 'Core Concepts and Skills', 16, 246, '8.5x11', '978-1-4533-2360-1', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('quirk', 'eMarketing', 'The Essential Guide to Online Marketing', 13, 291, '8.5x11', '978-1-936126-32-3', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('richmond', 'The Power of Selling', NULL, 13, 472, '8.5x11', NULL, '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('rittenberg', 'Principles of Microeconomics', NULL, 6, 551, '8.5x11', '978-0-9820430-3-5', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('siegel', 'Personal Finance', NULL, 8, 367, '8.5x11', NULL, '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('solomon', 'Launch!', 'Advertising and Promotion in Real Time', 13, 318, '8.5x11', '978-0-9820430-2-8', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('suranovic', 'International Economics', 'Theory and Policy', 6, 614, '8.5x11', '978-1-936126-42-2', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('tanner', 'Principles of Marketing', NULL, 13, 349, '8.5x11', NULL, '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('wright', 'Money and Banking', NULL, 6, 300, '8.5x11', '978-0-9820430-8-0', '2010-10-27 12:25:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('stangor', 'Introduction to Psychology', NULL, 16, 482, '8.5x11', '978-1-936126-48-4', '2010-11-04 13:08:10');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('redden', 'Elementary Algebra', NULL, 14, 655, '8.5x11', '978-1-4533-0092-3', '2010-11-04 13:10:09');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('eldridge', NULL, NULL, 0, 0, '8.5x11', NULL, '2010-12-07 15:39:56');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('lau', 'The Legal and Ethical Environment of Business', NULL, 3, 258, '8.5x11', '978-1-936126-58-3', '2010-12-08 15:13:14');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('brusseau', 'The Business Ethics Workshop', NULL, 18, 415, '8.5x11', '978-1-936126-38-5', '2010-12-09 12:55:09');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('averill', 'General Chemistry', 'Principles, Patterns, and Applications', 4, 1740, '8.5x11', '978-1-4533-1318-3', '2010-12-15 16:41:07');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('barkan', 'Sociology', 'Understanding and Changing the Social World, Comprehensive Edition', 0, 496, '8.5x11', '978-1-936126-52-1', '2010-12-16 13:27:12');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('trowbridge2', 'A History of the United States, Volume 2', NULL, 0, 546, '8.5x11', '978-1-4533-2609-1', '2011-01-12 10:40:05');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('ball', 'Introductory Chemistry', NULL, 0, 484, '8.5x11', '978-1-4533-1107-3', '2011-02-01 14:33:54');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('manzo', 'Introduction to Computing', NULL, 0, 36, '8.5x11', NULL, '2011-02-08 11:26:30');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('fallows', 'Exploring Perspectives', 'A Concise Guide to Analysis', 0, 98, '6x9', '978-1-4533-1145-5', '2011-02-10 18:00:21');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('tye', 'Sexuality & Our Diversity', 'Integrating Culture with the Biopsychosocial', 0, 38, '8.5x11', NULL, '2011-02-15 14:00:04');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('frost', 'Business Information Systems', 'Design an App for That', 0, 255, '8.5x11', '978-1-4533-1157-8', '2011-02-23 14:26:13');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('berglee', 'World Regional Geography', 'People, Places, and Globalization', 0, 580, '8.5x11', '978-1-4533-2336-6', '2011-03-01 14:56:01');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('portolesedias', 'Human Resource Management', NULL, 0, 360, '8.5x11', '978-1-4533-1943-7', '2011-03-09 15:12:56');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('cadden', 'Small Business Management in the 21st Century', NULL, 0, 520, '8.5x11', '978-1-4533-4554-2', '2011-03-11 14:00:40');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('pike', 'Elements of Chemistry and Technology', NULL, 0, 39, '8.5x11', NULL, '2011-03-16 15:46:54');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('ketchen', 'Mastering Strategic Management', NULL, 0, 292, '8.5x11', '978-1-4533-2310-6', '2011-04-01 07:29:33');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('overtree', 'Abnormal Psychology', NULL, 0, 83, '8.5x11', NULL, '2011-04-01 10:05:10');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('gittell', 'The Sustainable Business Case Book', NULL, 0, 322, '8.5x11', '978-1-4533-4675-4', '2011-04-06 13:18:24');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('ceniza', 'Six Steps to Job Search Success', NULL, 0, 301, '8.5x11', '978-1-4533-1725-9', '2011-04-08 08:35:22');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('larson', 'Sustainability, Innovation, and Entrepreneurship', NULL, 0, 312, '8.5x11', '978-1-4533-1412-8', '2011-04-13 21:08:45');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('shafer', 'Introductory Statistics', NULL, 0, 390, '8.5x11', '978-1-4533-4485-9', '2011-04-18 09:24:31');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('paustian', 'Through the Microscope', 'A Look at All Things Small', 0, 116, '8.5x11', NULL, '2011-04-21 12:14:03');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('blackstone', 'Principles of Sociological Inquiry', 'Qualitative and Quantitative Methods', 0, 236, '8.5x11', '978-1-4533-2338-0', '2011-05-12 16:37:48');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('gensler', 'Essentials of Statistics for Business and Economics', NULL, 0, 46, '8.5x11', NULL, '2011-05-16 13:33:09');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('zimmerman', 'Essentials of Nutrition', 'A Functional Approach', 0, 492, '8.5x11', '978-1-4533-5245-8', '2011-05-24 13:58:13');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('wrench', 'Stand Up, Speak Out', 'The Practice and Ethics of Public Speaking', 5, 350, '8.5x11', '978-1-4533-1225-4', '2011-05-31 11:57:06');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('krauter', 'Practical Genetics for the 21st Century', NULL, 2, 44, '8.5x11', '978-1-936126-40-8', '2011-05-31 12:06:55');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('paletz', 'American Government and Politics in the Information Age', NULL, 0, 450, '8.5x11', '978-1-4533-1498-2', '2011-05-31 12:20:06');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('campbell', 'Essentials of Geographic Information Systems', NULL, 10, 170, '8.5x11', '978-1-4533-2196-6', '2011-05-31 12:47:32');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('watkins', 'Microfinance', NULL, 8, 0, '8.5x11', NULL, '2011-06-01 13:18:10');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('lule', 'Understanding Media and Culture: An Introduction to Mass Communication', NULL, 0, 452, '8.5x11', '978-1-4533-2639-8', '2011-06-01 14:27:44');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('white', 'health', NULL, 0, 50, '8.5x11', NULL, '2011-06-06 16:08:03');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('baylor', 'Marriage and Family As It Is Lived', NULL, 0, 38, '8.5x11', NULL, '2011-06-10 16:03:28');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('cook', 'Foundations of Music Theory', 'Fundamental Concepts in the Language of Music', 0, 58, '8.5x11', NULL, '2011-06-17 10:39:13');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('jones', 'Communication in the Real World', 'An Introduction to Communication Studies', 0, 72, '8.5x11', NULL, '2011-06-28 14:07:02');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('mayer', 'Business Law and the Legal Environment', NULL, 0, 1210, '8.5x11', '978-1-4533-0516-4', '2011-07-28 09:56:11');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('storm', 'Criminal Law', NULL, 0, 398, '8.5x11', '978-1-4533-2412-7', '2011-07-28 10:27:06');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('scott', 'Precalculus: A Preparation for Calculus', NULL, 0, 154, '8.5x11', NULL, '2011-07-28 10:57:19');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('heisinger', 'Managerial Accounting', NULL, 0, 658, '8.5x11', '978-1-4533-4527-6', '2011-07-29 19:13:08');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('march', 'Elementary Spanish', NULL, 0, 73, '8.5x11', NULL, '2011-08-22 10:53:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('haruta', 'Technical Communication: Excelling in a Technological World', NULL, 0, 64, '8.5x11', NULL, '2011-08-24 16:43:14');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('shin', NULL, NULL, 0, 0, '8.5x11', NULL, '2011-08-25 17:21:07');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('pennington', 'Writing about Literature through Theory', NULL, 0, 270, '8.5x11', NULL, '2011-10-31 13:20:57');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('stengel', 'Principles of Managerial Economics', NULL, 0, 148, '6x9', '978-1-4533-2356-4', '2011-12-07 21:24:38');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('bowen', 'Mastering Public Relations', NULL, 0, 168, '6x9', '978-1-4533-2358-8', '2011-12-07 21:25:14');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('sanders', 'Developing New Products and Services', NULL, 0, 326, '6x9', '978-1-4533-2524-7', '2011-12-07 21:25:23');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('moua', 'Leading with Cultural Intelligence', NULL, 0, 170, '6x9', '978-1-4533-2588-9', '2011-12-07 21:25:36');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('judge', 'Focusing on Organizational Change', NULL, 0, 160, '6x9', '978-1-4533-2482-0', '2011-12-07 21:25:42');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('warren', 'Building Strategy and Performance', NULL, 0, 126, '6x9', '978-1-4533-2446-2', '2011-12-07 21:26:20');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('landrum', 'A Primer on Sustainable Business', NULL, 0, 194, '6x9', '978-1-4533-2584-1', '2011-12-07 21:26:36');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('dekluyverglobstrat', 'Fundamentals of Global Strategy', NULL, 0, 212, '6x9', '978-1-4533-2586-5', '2011-12-07 21:28:29');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('dekluyvercorpgov', 'Corporate Governance', NULL, 0, 196, '6x9', '978-1-4533-2590-2', '2011-12-07 21:28:54');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('urbany', 'Growth and Competitive Strategy in 3 Circles', NULL, 0, 180, '6x9', '978-1-4533-2582-7', '2011-12-07 21:29:35');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('lowe', 'Survey of British Literature', NULL, 0, 22, '8.5x11', NULL, '2011-12-20 22:28:03');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('gray', 'Public Relations', NULL, 0, 48, '8.5x11', NULL, '2011-12-20 23:42:18');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('sell', 'An Introduction to Politics', NULL, 0, 30, '8.5x11', NULL, '2012-01-11 11:06:29');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('sharp', 'International Relations Today', 'An Introduction', 0, 0, '8.5x11', NULL, '2012-02-08 11:25:17');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('hudson', 'What?s Your Point?', NULL, 0, 64, '8.5x11', NULL, '2012-04-25 22:57:32');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('sirgy', 'Consumer Behavior Today', NULL, 0, 44, '8.5x11', NULL, '2012-05-08 12:11:51');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('venditti', 'Exploring Group Communication', NULL, 0, 30, '8.5x11', NULL, '2012-06-06 11:10:44');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('schirr', 'Social Media Marketing', NULL, 0, 56, '8.5x11', NULL, '2012-09-14 14:30:21');
insert into vlibtests.books (book_name, title, subtitle, discipline_id, num_pages, book_size, isbn, created) values ('ingersoll', 'Theories of Personality', 'Engagement through Personal Exploration', 0, 40, '8.5x11', NULL, '2012-09-28 11:43:42');

