select
   b.id, b.name, b.published, bt.nme as book_type, ft.name as fiction_name
from
   books b
   join book_types bt on b.book_type_id = bt.id
   left join fiction_type ft on b.fiction_type = ft.id
   left outer join fiction_type ft on b.fiction_type = ft.id
   right join fiction_type ft on b.fiction_type = ft.id
   inner join fiction_type ft on b.fiction_type = ft.id
where
   bt.id in (10,20,30);
