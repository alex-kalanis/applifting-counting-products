"""empty message

Revision ID: 1fa33c8cdbc8
Revises: 
Create Date: 2023-06-01 16:56:47.227904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fa33c8cdbc8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # clearing
    op.execute('DROP TABLE IF EXISTS "product_offers";')
    op.execute('DROP TABLE IF EXISTS "products";')
    op.execute('DROP TABLE IF EXISTS "configs";')
    op.execute('DROP TABLE IF EXISTS "users";')
    # new ones
    op.execute('CREATE TABLE "configs" ( "id" serial NOT NULL, PRIMARY KEY ("id"), "key" character varying(64) NOT NULL, "value" character varying(1024) NULL ); COMMENT ON TABLE "configs" IS \'Configuration\';')
    op.execute('ALTER TABLE "configs" ADD CONSTRAINT "configs_key" UNIQUE ("key");')
    op.execute('CREATE TABLE "users" ( "id" serial NOT NULL, PRIMARY KEY ("id"), "name" character varying(64) NOT NULL, "token" character varying(256) NOT NULL, "deleted" timestamp NULL );')
    op.execute('CREATE INDEX "users_token" ON "users" ("token"); CREATE INDEX "users_deleted" ON "users" ("deleted");')
    op.execute('CREATE TABLE "products" ( "id" serial NOT NULL, PRIMARY KEY ("id"), "uuid" character varying(64) NOT NULL, "name" character varying(64) NOT NULL, "desc" character varying(256) NOT NULL, "deleted" timestamp NULL ); COMMENT ON TABLE "products" IS \'Available products\';')
    op.execute('ALTER TABLE "products" ADD CONSTRAINT "products_uuid" UNIQUE ("uuid"); CREATE INDEX "products_name" ON "products" ("name"); CREATE INDEX "products_deleted" ON "products" ("deleted");')
    op.execute('CREATE TABLE "product_offers" ( "id" serial NOT NULL, PRIMARY KEY ("id"), "product_id" integer NOT NULL, "price" integer NOT NULL, "pieces" integer NOT NULL, "added" timestamp NOT NULL ); COMMENT ON TABLE "product_offers" IS \'Offers for known products\';')
    op.execute('ALTER TABLE "product_offers" ADD FOREIGN KEY ("product_id") REFERENCES "products" ("id") ON DELETE CASCADE ON UPDATE CASCADE;')
    op.execute('CREATE INDEX "product_offers_product_id" ON "product_offers" ("product_id"); CREATE INDEX "product_offers_added" ON "product_offers" ("added");')

def downgrade():
    op.execute('DROP TABLE IF EXISTS "product_offers";')
    op.execute('DROP TABLE IF EXISTS "products";')
    op.execute('DROP TABLE IF EXISTS "users";')
    op.execute('DROP TABLE IF EXISTS "configs";')
