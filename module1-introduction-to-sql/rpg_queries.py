# module1-introduction-to-sql.py

import os
import sqlite3

DB_FILEPATH = os.path.join(os.path.dirname(__file__),
                                           "..",
                                           "module1-introduction-to-sql",
                                           "rpg_db.sqlite3")

conn = sqlite3.connect(DB_FILEPATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

total_characters = """
SELECT count(distinct character_id)
FROM charactercreator_character;
"""

# How many total Characters are there?
# total_characters = 302
total_characters_result = cur.execute(total_characters).fetchall()
print("Total Characters:", total_characters_result[0][0])

# How many [characters] of each specific subclass?
char_per_subclass = """
SELECT

	count(distinct f.character_ptr_id) as total_fighters 
	,count(distinct c.character_ptr_id) as total_clerics
	,count(distinct m.character_ptr_id) as total_mages
	,count(distinct n.mage_ptr_id) as total_necromancers
	,count(distinct t.character_ptr_id) as total_thief
	
FROM charactercreator_character ccc
LEFT JOIN charactercreator_fighter f on ccc.character_id = f.character_ptr_id
LEFT JOIN charactercreator_cleric c on ccc.character_id = c.character_ptr_id
LEFT JOIN charactercreator_mage m on ccc.character_id = m.character_ptr_id
LEFT JOIN charactercreator_necromancer n on ccc.character_id = n.mage_ptr_id
LEFT JOIN charactercreator_thief t on ccc.character_id = t.character_ptr_id;
"""
char_per_subclass_result = cur.execute(char_per_subclass).fetchall()

classes = ['Fighters', 'Clerics', 'Mages', 'Necromancers', 'Thieves']

for i in range(0, 5):
    print(f"Total {classes[i]}:", char_per_subclass_result[0][i])


# How many total items?
# total_items = 898
total_items = """
SELECT SUM(item_count)
FROM(
	SELECT
	c.character_id
	,c."name" as character_name
	,count(distinct inv.item_id) as item_count 
	FROM charactercreator_character c
	LEFT JOIN charactercreator_character_inventory inv
	ON c.character_id = inv.character_id
	GROUP BY 1, 2
) item_count_subq;
"""

total_items_result = cur.execute(total_items).fetchall()
print("Total Items:", total_items_result[0][0])


# How many of the Items are weapons?
# total_weapons = 203
total_weapons = """
SELECT
	count(item_id)
FROM(
	SELECT
		c.character_id,
		inv.item_id
	FROM charactercreator_character c
	LEFT JOIN charactercreator_character_inventory inv
	ON c.character_id = inv.character_id
	LEFT JOIN  armory_item
	ON inv.item_id = armory_item.item_id
	JOIN armory_weapon
	ON armory_item.item_id = armory_weapon.item_ptr_id
	) weapons;
"""

total_weapons_result = cur.execute(total_weapons).fetchall()
print("Total Weapons:", total_weapons_result[0][0])


# How many total non-weapon items are there?
# total_non_weapons = 695
total_non_weapons = """
SELECT
	sum(non_weapon_count)
	FROM(
	SELECT
		item_count,
		weapon_count,
		item_count - weapon_count non_weapon_count
	FROM(
		SELECT
			ch.character_id,
			ch."name" as char_name,
			count(distinct inv.item_id) item_count,
			count(distinct w.item_ptr_id) weapon_count
		FROM charactercreator_character ch
		LEFT JOIN charactercreator_character_inventory inv 
		ON ch.character_id = inv.character_id
		LEFT JOIN armory_weapon w
		ON inv.item_id = w.item_ptr_id
		GROUP BY 1, 2
		));
"""

total_non_weapons_result = cur.execute(total_non_weapons).fetchall()
print("Total Non-Weapon Items:", total_non_weapons_result[0][0], '\n')


# How many Items does each character have? (Return first 20 rows)
top_20_items = """
SELECT
	c.character_id
	,c."name" as character_name
	,count(distinct inv.item_id) as item_count 
FROM charactercreator_character c
LEFT JOIN charactercreator_character_inventory inv
ON c.character_id = inv.character_id
GROUP BY 1, 2
LIMIT 20;
"""

print('charachter_name,', 'item_count')
print('---------------------------')
top_20_items_results = cur.execute(top_20_items).fetchall()
for row in top_20_items_results:
    print(row["character_name"], row["item_count"])


# How many Weapons does each character have? (Return first 20 rows)
top_20_weapons = """
SELECT
	char_name,
	weapon_count
FROM(
	SELECT
	ch.character_id,
	ch."name" as char_name,
	count(distinct inv.item_id) item_count,
	count(distinct w.item_ptr_id) weapon_count
	FROM charactercreator_character ch
	LEFT JOIN charactercreator_character_inventory inv 
	ON ch.character_id = inv.character_id
	LEFT JOIN armory_weapon w
	ON inv.item_id = w.item_ptr_id
	GROUP BY 1, 2
	LIMIT 20
	)
"""

print('')
print('char_name, weapon_count')
print('-----------------------')
top_20_weapons_results = cur.execute(top_20_weapons).fetchall()

for row in top_20_weapons_results:
    print(row["char_name"], row["weapon_count"])

# On average, how many Items does each Character have?
# On average, how many Weapons does each Character have?
# avg_items = 2.97
# avg_weapons = 0.67
avg_items = """
SELECT
	round(avg(item_count), 2),
	round(avg(weapon_count), 2)
FROM(
	SELECT
		ch.character_id,
		ch."name" as char_name,
		count(distinct inv.item_id) item_count,
		count(distinct w.item_ptr_id) weapon_count
	FROM charactercreator_character ch
	LEFT JOIN charactercreator_character_inventory inv 
	ON ch.character_id = inv.character_id
	LEFT JOIN armory_weapon w
	ON inv.item_id = w.item_ptr_id
	GROUP BY 1, 2
	) averages;
"""

item_types = ['Items', 'Weapons']
avg_items_results = cur.execute(avg_items).fetchall()

print('')
for i in range(0, 2):
    print(f"Average {item_types[i]}: {avg_items_results[0][i]}")
