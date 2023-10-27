"""initial migration

Revision ID: 385a2342ad9d
Revises: 
Create Date: 2023-10-10 15:05:41.825878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '385a2342ad9d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('age_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_age_group_id'), 'age_group', ['id'], unique=False)
    op.create_table('class_',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_name', sa.String(), nullable=False),
    sa.Column('key_gbif', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_gbif')
    )
    op.create_index(op.f('ix_class__class_name'), 'class_', ['class_name'], unique=True)
    op.create_index(op.f('ix_class__id'), 'class_', ['id'], unique=False)
    op.create_table('flora_relocation_zone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flora_relocation_zone_id'), 'flora_relocation_zone', ['id'], unique=False)
    op.create_index(op.f('ix_flora_relocation_zone_name'), 'flora_relocation_zone', ['name'], unique=False)
    op.create_table('flora_rescue_zone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flora_rescue_zone_description'), 'flora_rescue_zone', ['description'], unique=False)
    op.create_index(op.f('ix_flora_rescue_zone_id'), 'flora_rescue_zone', ['id'], unique=False)
    op.create_index(op.f('ix_flora_rescue_zone_name'), 'flora_rescue_zone', ['name'], unique=False)
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status_name', sa.String(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_status_id'), 'status', ['id'], unique=False)
    op.create_index(op.f('ix_status_status_name'), 'status', ['status_name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('permissions', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_name', sa.String(), nullable=False),
    sa.Column('key_gbif', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('class__id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class__id'], ['class_.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_gbif')
    )
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=False)
    op.create_index(op.f('ix_order_order_name'), 'order', ['order_name'], unique=True)
    op.create_table('family',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('family_name', sa.String(), nullable=False),
    sa.Column('key_gbif', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_gbif')
    )
    op.create_index(op.f('ix_family_family_name'), 'family', ['family_name'], unique=True)
    op.create_index(op.f('ix_family_id'), 'family', ['id'], unique=False)
    op.create_table('genus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genus_name', sa.String(), nullable=False),
    sa.Column('genus_full_name', sa.String(), nullable=True),
    sa.Column('key_gbif', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_gbif')
    )
    op.create_index(op.f('ix_genus_genus_full_name'), 'genus', ['genus_full_name'], unique=True)
    op.create_index(op.f('ix_genus_genus_name'), 'genus', ['genus_name'], unique=True)
    op.create_index(op.f('ix_genus_id'), 'genus', ['id'], unique=False)
    op.create_table('species',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scientific_name', sa.String(), nullable=False),
    sa.Column('specific_epithet', sa.String(), nullable=False),
    sa.Column('key_gbif', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('genus_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genus_id'], ['genus.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_gbif')
    )
    op.create_index(op.f('ix_species_id'), 'species', ['id'], unique=False)
    op.create_index(op.f('ix_species_scientific_name'), 'species', ['scientific_name'], unique=True)
    op.create_index(op.f('ix_species_specific_epithet'), 'species', ['specific_epithet'], unique=False)
    op.create_table('flora_rescue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('epiphyte_number', sa.Integer(), nullable=False),
    sa.Column('rescue_date', sa.DateTime(), nullable=False),
    sa.Column('rescue_area_latitude', sa.Float(), nullable=False),
    sa.Column('rescue_area_longitude', sa.Float(), nullable=False),
    sa.Column('substrate', sa.String(), nullable=True),
    sa.Column('dap_bryophyte', sa.Float(), nullable=True),
    sa.Column('height_bryophyte', sa.Float(), nullable=True),
    sa.Column('bryophyte_position', sa.Integer(), nullable=True),
    sa.Column('growth_habit', sa.String(), nullable=False),
    sa.Column('epiphyte_phenology', sa.String(), nullable=False),
    sa.Column('health_status_epiphyte', sa.String(), nullable=False),
    sa.Column('microhabitat', sa.String(), nullable=False),
    sa.Column('other_observations', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('specie_bryophyte_id', sa.Integer(), nullable=True),
    sa.Column('specie_epiphyte_id', sa.Integer(), nullable=False),
    sa.Column('genus_bryophyte_id', sa.Integer(), nullable=True),
    sa.Column('family_bryophyte_id', sa.Integer(), nullable=True),
    sa.Column('rescue_zone_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['family_bryophyte_id'], ['family.id'], ),
    sa.ForeignKeyConstraint(['genus_bryophyte_id'], ['genus.id'], ),
    sa.ForeignKeyConstraint(['rescue_zone_id'], ['flora_rescue_zone.id'], ),
    sa.ForeignKeyConstraint(['specie_bryophyte_id'], ['species.id'], ),
    sa.ForeignKeyConstraint(['specie_epiphyte_id'], ['species.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flora_rescue_bryophyte_position'), 'flora_rescue', ['bryophyte_position'], unique=False)
    op.create_index(op.f('ix_flora_rescue_dap_bryophyte'), 'flora_rescue', ['dap_bryophyte'], unique=False)
    op.create_index(op.f('ix_flora_rescue_epiphyte_number'), 'flora_rescue', ['epiphyte_number'], unique=False)
    op.create_index(op.f('ix_flora_rescue_epiphyte_phenology'), 'flora_rescue', ['epiphyte_phenology'], unique=False)
    op.create_index(op.f('ix_flora_rescue_growth_habit'), 'flora_rescue', ['growth_habit'], unique=False)
    op.create_index(op.f('ix_flora_rescue_health_status_epiphyte'), 'flora_rescue', ['health_status_epiphyte'], unique=False)
    op.create_index(op.f('ix_flora_rescue_height_bryophyte'), 'flora_rescue', ['height_bryophyte'], unique=False)
    op.create_index(op.f('ix_flora_rescue_id'), 'flora_rescue', ['id'], unique=False)
    op.create_index(op.f('ix_flora_rescue_microhabitat'), 'flora_rescue', ['microhabitat'], unique=False)
    op.create_index(op.f('ix_flora_rescue_other_observations'), 'flora_rescue', ['other_observations'], unique=False)
    op.create_index(op.f('ix_flora_rescue_rescue_area_latitude'), 'flora_rescue', ['rescue_area_latitude'], unique=False)
    op.create_index(op.f('ix_flora_rescue_rescue_area_longitude'), 'flora_rescue', ['rescue_area_longitude'], unique=False)
    op.create_index(op.f('ix_flora_rescue_substrate'), 'flora_rescue', ['substrate'], unique=False)
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('atribute', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('species_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['species_id'], ['species.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_images_atribute'), 'images', ['atribute'], unique=False)
    op.create_index(op.f('ix_images_id'), 'images', ['id'], unique=False)
    op.create_index(op.f('ix_images_url'), 'images', ['url'], unique=False)
    op.create_table('rescue_herpetofauna',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('rescue_date_in', sa.DateTime(), nullable=False),
    sa.Column('rescue_date_out', sa.DateTime(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('altitude', sa.Integer(), nullable=False),
    sa.Column('individual_count', sa.Integer(), nullable=True),
    sa.Column('gender', sa.Boolean(), nullable=True),
    sa.Column('age_group_id', sa.Integer(), nullable=True),
    sa.Column('specie_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['age_group_id'], ['age_group.id'], ),
    sa.ForeignKeyConstraint(['specie_id'], ['species.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rescue_herpetofauna_id'), 'rescue_herpetofauna', ['id'], unique=False)
    op.create_table('flora_relocation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('relocation_date', sa.DateTime(), nullable=False),
    sa.Column('size', sa.Float(), nullable=False),
    sa.Column('epiphyte_phenology', sa.String(), nullable=False),
    sa.Column('johanson_zone', sa.String(), nullable=True),
    sa.Column('relocation_position_latitude', sa.Float(), nullable=False),
    sa.Column('relocation_position_longitude', sa.Float(), nullable=False),
    sa.Column('bryophyte_number', sa.Integer(), nullable=False),
    sa.Column('dap_bryophyte', sa.Float(), nullable=True),
    sa.Column('height_bryophyte', sa.Float(), nullable=True),
    sa.Column('bark_type', sa.String(), nullable=True),
    sa.Column('infested_lianas', sa.String(), nullable=True),
    sa.Column('relocation_number', sa.Integer(), nullable=True),
    sa.Column('other_observations', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('flora_rescue_id', sa.Integer(), nullable=False),
    sa.Column('specie_bryophyte_id', sa.Integer(), nullable=True),
    sa.Column('genus_bryophyte_id', sa.Integer(), nullable=True),
    sa.Column('family_bryophyte_id', sa.Integer(), nullable=True),
    sa.Column('relocation_zone_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['family_bryophyte_id'], ['family.id'], ),
    sa.ForeignKeyConstraint(['flora_rescue_id'], ['flora_rescue.id'], ),
    sa.ForeignKeyConstraint(['genus_bryophyte_id'], ['genus.id'], ),
    sa.ForeignKeyConstraint(['relocation_zone_id'], ['flora_relocation_zone.id'], ),
    sa.ForeignKeyConstraint(['specie_bryophyte_id'], ['species.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flora_relocation_bark_type'), 'flora_relocation', ['bark_type'], unique=False)
    op.create_index(op.f('ix_flora_relocation_bryophyte_number'), 'flora_relocation', ['bryophyte_number'], unique=False)
    op.create_index(op.f('ix_flora_relocation_dap_bryophyte'), 'flora_relocation', ['dap_bryophyte'], unique=False)
    op.create_index(op.f('ix_flora_relocation_epiphyte_phenology'), 'flora_relocation', ['epiphyte_phenology'], unique=False)
    op.create_index(op.f('ix_flora_relocation_height_bryophyte'), 'flora_relocation', ['height_bryophyte'], unique=False)
    op.create_index(op.f('ix_flora_relocation_id'), 'flora_relocation', ['id'], unique=False)
    op.create_index(op.f('ix_flora_relocation_infested_lianas'), 'flora_relocation', ['infested_lianas'], unique=False)
    op.create_index(op.f('ix_flora_relocation_johanson_zone'), 'flora_relocation', ['johanson_zone'], unique=False)
    op.create_index(op.f('ix_flora_relocation_other_observations'), 'flora_relocation', ['other_observations'], unique=False)
    op.create_index(op.f('ix_flora_relocation_relocation_number'), 'flora_relocation', ['relocation_number'], unique=False)
    op.create_index(op.f('ix_flora_relocation_relocation_position_latitude'), 'flora_relocation', ['relocation_position_latitude'], unique=False)
    op.create_index(op.f('ix_flora_relocation_relocation_position_longitude'), 'flora_relocation', ['relocation_position_longitude'], unique=False)
    op.create_index(op.f('ix_flora_relocation_size'), 'flora_relocation', ['size'], unique=False)
    op.create_table('plant_nursery',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('entry_date', sa.DateTime(), nullable=False),
    sa.Column('cod_reg', sa.String(), nullable=False),
    sa.Column('health_status_epiphyte', sa.String(), nullable=False),
    sa.Column('vegetative_state', sa.String(), nullable=False),
    sa.Column('flowering_date', sa.DateTime(), nullable=False),
    sa.Column('treatment_product', sa.String(), nullable=False),
    sa.Column('is_pruned', sa.Boolean(), nullable=False),
    sa.Column('is_phytosanitary_treatment', sa.Boolean(), nullable=False),
    sa.Column('substrate', sa.String(), nullable=False),
    sa.Column('departure_date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('flora_rescue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['flora_rescue_id'], ['flora_rescue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plant_nursery_cod_reg'), 'plant_nursery', ['cod_reg'], unique=False)
    op.create_index(op.f('ix_plant_nursery_health_status_epiphyte'), 'plant_nursery', ['health_status_epiphyte'], unique=False)
    op.create_index(op.f('ix_plant_nursery_id'), 'plant_nursery', ['id'], unique=False)
    op.create_index(op.f('ix_plant_nursery_substrate'), 'plant_nursery', ['substrate'], unique=False)
    op.create_index(op.f('ix_plant_nursery_treatment_product'), 'plant_nursery', ['treatment_product'], unique=False)
    op.create_index(op.f('ix_plant_nursery_vegetative_state'), 'plant_nursery', ['vegetative_state'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_plant_nursery_vegetative_state'), table_name='plant_nursery')
    op.drop_index(op.f('ix_plant_nursery_treatment_product'), table_name='plant_nursery')
    op.drop_index(op.f('ix_plant_nursery_substrate'), table_name='plant_nursery')
    op.drop_index(op.f('ix_plant_nursery_id'), table_name='plant_nursery')
    op.drop_index(op.f('ix_plant_nursery_health_status_epiphyte'), table_name='plant_nursery')
    op.drop_index(op.f('ix_plant_nursery_cod_reg'), table_name='plant_nursery')
    op.drop_table('plant_nursery')
    op.drop_index(op.f('ix_flora_relocation_size'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_relocation_position_longitude'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_relocation_position_latitude'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_relocation_number'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_other_observations'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_johanson_zone'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_infested_lianas'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_id'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_height_bryophyte'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_epiphyte_phenology'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_dap_bryophyte'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_bryophyte_number'), table_name='flora_relocation')
    op.drop_index(op.f('ix_flora_relocation_bark_type'), table_name='flora_relocation')
    op.drop_table('flora_relocation')
    op.drop_index(op.f('ix_rescue_herpetofauna_id'), table_name='rescue_herpetofauna')
    op.drop_table('rescue_herpetofauna')
    op.drop_index(op.f('ix_images_url'), table_name='images')
    op.drop_index(op.f('ix_images_id'), table_name='images')
    op.drop_index(op.f('ix_images_atribute'), table_name='images')
    op.drop_table('images')
    op.drop_index(op.f('ix_flora_rescue_substrate'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_rescue_area_longitude'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_rescue_area_latitude'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_other_observations'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_microhabitat'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_id'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_height_bryophyte'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_health_status_epiphyte'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_growth_habit'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_epiphyte_phenology'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_epiphyte_number'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_dap_bryophyte'), table_name='flora_rescue')
    op.drop_index(op.f('ix_flora_rescue_bryophyte_position'), table_name='flora_rescue')
    op.drop_table('flora_rescue')
    op.drop_index(op.f('ix_species_specific_epithet'), table_name='species')
    op.drop_index(op.f('ix_species_scientific_name'), table_name='species')
    op.drop_index(op.f('ix_species_id'), table_name='species')
    op.drop_table('species')
    op.drop_index(op.f('ix_genus_id'), table_name='genus')
    op.drop_index(op.f('ix_genus_genus_name'), table_name='genus')
    op.drop_index(op.f('ix_genus_genus_full_name'), table_name='genus')
    op.drop_table('genus')
    op.drop_index(op.f('ix_family_id'), table_name='family')
    op.drop_index(op.f('ix_family_family_name'), table_name='family')
    op.drop_table('family')
    op.drop_index(op.f('ix_order_order_name'), table_name='order')
    op.drop_index(op.f('ix_order_id'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_status_status_name'), table_name='status')
    op.drop_index(op.f('ix_status_id'), table_name='status')
    op.drop_table('status')
    op.drop_index(op.f('ix_flora_rescue_zone_name'), table_name='flora_rescue_zone')
    op.drop_index(op.f('ix_flora_rescue_zone_id'), table_name='flora_rescue_zone')
    op.drop_index(op.f('ix_flora_rescue_zone_description'), table_name='flora_rescue_zone')
    op.drop_table('flora_rescue_zone')
    op.drop_index(op.f('ix_flora_relocation_zone_name'), table_name='flora_relocation_zone')
    op.drop_index(op.f('ix_flora_relocation_zone_id'), table_name='flora_relocation_zone')
    op.drop_table('flora_relocation_zone')
    op.drop_index(op.f('ix_class__id'), table_name='class_')
    op.drop_index(op.f('ix_class__class_name'), table_name='class_')
    op.drop_table('class_')
    op.drop_index(op.f('ix_age_group_id'), table_name='age_group')
    op.drop_table('age_group')
    # ### end Alembic commands ###
