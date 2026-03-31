CREATE TABLE public.opinioes (
	id serial4 NOT NULL,
	nome varchar(100) NULL,
	email varchar(150) NULL,
	mensagem text NULL,
	avaliacao int4 NULL,
	CONSTRAINT opinioes_pkey PRIMARY KEY (id)
);