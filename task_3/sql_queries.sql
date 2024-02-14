1
select  c.category_id , c.name, count(fc.film_id) as number_of_films
from film_category fc
left join category c using (category_id)
group by c.category_id ,c.name
ORDER by number_of_films  desc


2
select a.actor_id ,
a.first_name || '  ' || a.last_name as name_of_actor ,
count(r.rental_id ) as number_of_rent
from actor a
join film_actor fa using(actor_id)
join inventory i using(film_id)
join rental r using(inventory_id)
group by a.actor_id, name_of_actor
order by number_of_rent desc
limit 10

3
select c.name, c.category_id ,
sum(p.amount ) as total_spent
from payment p
join rental r using(rental_id)
join inventory i using(inventory_id)
join film_category fc using(film_id)
join category c using(category_id)
group by c.name, c.category_id
order by total_spent desc
limit 1


4
select f.film_id, f.title
from film f
where not exists
    (select i.film_id from  inventory i where f.film_id = i.film_id)


5
with cat_children as (
	select a.first_name || ' ' || a.last_name as actors_name,
    count(*) as times_in_category,
    dense_rank() over ( order by count(*) desc) as place_in_top
    from actor a
    join film_actor fa using(actor_id)
    join film_category fc using(film_id)
    join category c on using(category_id)
    where c.name = 'Children'
    group by a.first_name, a.last_name, c.name
    order by times_in_category desc)
select *
from cat_children
where place_in_top<=3

6
select city.city,
count(case when customer.active = 1 then 1 end) as active_customers,
count(case when customer.active = 0 then 1 end) as not_active_customers
from city
left join address using(city_id)
join customer using(address_id)
group by city.city
order by not_active_customers desc, active_customers desc

7
with Rental_hours_category_city as
(
	select c.name as category_name,
		c3.city as city_name,
		(date_part('day', (r.return_date - r.rental_date)) * 24 + date_part('hour', (r.return_date - r.rental_date))) as hours_in_rental
	from rental r
	join inventory i using(inventory_id)
	join film_category fc using(film_id)
	join category c using(category_id)
	join customer c2 using(customer_id)
	join address a using(address_id)
	join city c3 using(city_id)
)
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


