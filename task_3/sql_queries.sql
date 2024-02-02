1
select  c.category_id , c.name, count(fc.film_id) as number_of_films
from film_category fc
left join category c on c.category_id = fc.category_id
group by c.category_id ,c.name
ORDER by number_of_films  desc


2
select a.actor_id ,
a.first_name || '  ' || a.last_name as name_of_actor ,
count(r.rental_id ) as number_of_rent
from actor a
join film_actor fa on a.actor_id =fa.actor_id
join inventory i on i.film_id = fa.film_id
join rental r on r.inventory_id =i.inventory_id
group by a.actor_id, name_of_actor
order by number_of_rent desc
limit 10

3
select c.name, c.category_id ,
sum(p.amount ) as total_spent
from payment p
join rental r on r.rental_id=p.rental_id
join inventory i on i.inventory_id =r.inventory_id
join film_category fc on i.film_id=fc.film_id
join category c on c.category_id =fc.category_id
group by c.name, c.category_id
order by total_spent desc

4
select f.film_id , f.title
from film f
left join inventory i on f.film_id=i.film_id
where i.film_id  is null

5
select *
from
    (select a.first_name || ' ' || a.last_name as actors_name,
    count(*) as times_in_category,
    dense_rank() over ( order by count(*) desc) as place_in_top
    from actor a
    join film_actor fa on fa.actor_id =a.actor_id
    join film_category fc on fa.film_id =fc.film_id
    join category c on fc.category_id =c.category_id
    where c.name = 'Children'
    group by a.first_name, a.last_name, c.name
    order by times_in_category desc) cat_children
where place_in_top<=3

6
select city.city,
count(case when customer.active = 1 then 1 end) as active_customers,
count(case when customer.active = 0 then 1 end) as not_active_customers
from city
left join address on city.city_id = address.city_id
join customer on address.address_id = customer.address_id
group by city.city
order by not_active_customers desc, active_customers desc

7
with Rental_hours_category_city as (
	select c.name as category_name,
		c3.city as city_name,
		(date_part('day', (r.return_date - r.rental_date)) * 24 + date_part('hour', (r.return_date - r.rental_date))) as hours_in_rental
	from rental r
	join inventory i on i.inventory_id = r.inventory_id
	join film_category fc on fc.film_id = i.film_id
	join category c on c.category_id =fc.category_id
	join customer c2 on c2.customer_id = r.customer_id
	join address a on a.address_id =c2.address_id
	join city c3 on c3.city_id =a.city_id )
--	the category of films that has the highest number of total rental hours in cities starting with the letter 'A'
(select sum(hours_in_rental) as total_hours_in_rental, category_name
from Rental_hours_category_city
where lower(city_name) like 'a%'
group by  category_name
order by total_hours_in_rental desc
limit 1)
union all
--	the category of films that has the highest number of total rental hours in cities with the '-'
(select sum(hours_in_rental) as total_hours_in_rental, category_name
from Rental_hours_category_city
where lower(city_name) like '%-%'
group by  category_name
order by total_hours_in_rental desc
limit 1)

