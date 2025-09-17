-- PGVector installation
CREATE EXTENSION IF NOT EXISTS vector;

-- Table to register the files already read

CREATE TABLE public.files_read (
	id bigserial NOT NULL,
	file_name varchar NOT NULL,
	CONSTRAINT files_read_pk PRIMARY KEY (id),
	CONSTRAINT files_read_unique UNIQUE (file_name)
);

-- Table to register the chunks of the files read

CREATE TABLE public.files_embedding (
	id bigserial NOT NULL,
	embedding public.vector NOT NULL,
	"content" varchar NOT NULL,
	files_read_id bigserial NOT NULL,
	CONSTRAINT files_embedding_pkey PRIMARY KEY (id)
);

ALTER TABLE public.files_embedding ADD CONSTRAINT fk_files_embedding_files_read FOREIGN KEY (files_read_id) REFERENCES public.files_read(id);