from py2neo import Node, Relationship


# 1- Initial Migration

def new_person(first_name, email, last_name, phone_number, address, birthday):
    return Node("Person",
                first_name=first_name,
                email=email,
                last_name=last_name,
                phone_number=phone_number,
                address=address,
                birthday=birthday)


def migrate(tx):
    tx.graph.schema.create_uniqueness_constraint('Person', 'email')

    # Tosh and Prisca - Grand Parent
    tosh = new_person('Tosh', 'tosh@tosh.com', 'Toshes', '222-222-4444', 'Toshes Home', '2019-10-12')
    prisca = new_person('Prisca', 'prisca@prisca.com', 'Toshes', '222-222-4444', 'Toshes Home', '2019-10-12')
    tx.create(tosh | prisca)

    # Joan's grand dad
    daniel = new_person('Daniel', 'daniel@daniel.com', 'Daniels', '122-222-4444', 'Daniels Home', '2019-10-12')
    tx.create(daniel)

    # mark and nancy family
    mark = new_person('Mark', 'mark@mark.com', 'Marks', '322-222-4444', 'Marks Home', '2019-10-12')
    nancy = new_person('Nance', 'nancy@nancy.com', 'Marks', '322-222-4444', 'Marks Home', '2019-10-12')
    nicole = new_person('Nicole', 'nicole@nicole.com', 'Marks', '322-222-4444', 'Marks Home', '2019-10-12')
    drew = new_person('Drew', 'drew@drew.com', 'Marks', '322-222-4444', 'Marks Home', '2019-10-12')
    mary = new_person('Mary', 'mary@mary.com', 'Marks', '322-222-4444', 'Marks Home', '2019-10-12')
    # nancy child's
    jakie = new_person('Jakie', 'jakie@jakie.com', 'Nancy', '422-222-4444', 'Marks Home', '2019-10-12')
    tx.create(mark | nancy | nicole | drew | mary | jakie)

    # jared and joan family
    jared = new_person('Jared', 'jared@jared.com', 'JaredHold', '522-222-4444', 'JaredHold Home', '2019-10-12')
    joan = new_person('Joan', 'joan@joan.com', 'JaredHold', '522-222-4444', 'JaredHold Home', '2019-10-12')
    gil = new_person('Gil', 'gil@gil.com', 'JaredHold', '522-222-4444', 'JaredHold Home', '2019-10-12')
    marcus = new_person('Marcus', 'marcus@marcus.com', 'JaredHold', '522-222-4444', 'JaredHold Home', '2019-10-12')
    tx.create(jared | joan | gil | marcus)

    # joan's sister family
    mercy = new_person('Mercy', 'mercy@mercy.com', 'Mercies', '422-222-4444', 'Mercies Home', '2019-10-12')
    jack = new_person('Jack', 'jack@jack.com', 'Mercies', '422-222-4444', 'Mercies Home', '2019-10-12')
    tx.create(mercy | jack)

    PARENT = Relationship.type("PARENT")
    MARRIED = Relationship.type("MARRIED")

    # Tosh and Prisca Marriage
    tx.create(MARRIED(tosh, prisca))
    # Tosh and Prisca children
    tx.create(PARENT(tosh, jared))
    tx.create(PARENT(tosh, mark))

    # Daniel's children
    tx.create(PARENT(daniel, joan))
    tx.create(PARENT(daniel, mercy))

    # mark and nancy married
    tx.create(MARRIED(mark, nancy))
    # mark and nancy children
    tx.create(PARENT(mark, nicole))
    tx.create(PARENT(mark, drew))
    tx.create(PARENT(mark, mary))
    tx.create(PARENT(nancy, nicole))
    tx.create(PARENT(nancy, drew))
    tx.create(PARENT(nancy, mary))
    tx.create(PARENT(nancy, jakie))

    # mark and nancy married
    tx.create(MARRIED(jared, joan))

    # jared and joan children
    tx.create(PARENT(jared, gil))
    tx.create(PARENT(jared, marcus))
    tx.create(PARENT(joan, gil))
    # marcus not listed as child of joan, to see if we can get him as a step child from marriage
    # tx.create(PARENT(joan, marcus))

    # mercy's family
    tx.create(PARENT(mercy, jack))
