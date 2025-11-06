CREATE DATABASE "DBprojetoFinal" /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

-- DBprojetoFinal.carrinho definition

CREATE TABLE "carrinho" (
  "id" int NOT NULL AUTO_INCREMENT,
  "id_utilizador" int NOT NULL,
  "id_produto" varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "quantidade" varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY ("id"),
  KEY "id_produto" ("id_produto"),
  KEY "carrinho_utilizador_FK" ("id_utilizador"),
  CONSTRAINT "carrinho_utilizador_FK" FOREIGN KEY ("id_utilizador") REFERENCES "utilizador" ("id") ON DELETE CASCADE
);

-- DBprojetoFinal.endereco definition

CREATE TABLE "endereco" (
  "id" int NOT NULL AUTO_INCREMENT,
  "id_utilizador" int NOT NULL,
  "email" varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  "telefone" bigint NOT NULL,
  "municipio" varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  "detalhes_rua" varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY ("id"),
  KEY "id_utilizador" ("id_utilizador"),
  CONSTRAINT "endereco_ibfk_1" FOREIGN KEY ("id_utilizador") REFERENCES "utilizador" ("id") ON DELETE CASCADE
);


-- DBprojetoFinal.historico definition

CREATE TABLE "historico" (
  "id" int NOT NULL AUTO_INCREMENT,
  "id_utilizador" int NOT NULL,
  "id_produtos" varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  "quantidades" varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  "data_compra" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "id_compra" varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  "total" int NOT NULL,
  "estado" varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "detalhes" varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY ("id"),
  KEY "id_utilizador" ("id_utilizador"),
  CONSTRAINT "historico_ibfk_1" FOREIGN KEY ("id_utilizador") REFERENCES "utilizador" ("id") ON DELETE CASCADE
);

-- DBprojetoFinal.mensagem definition

CREATE TABLE "mensagem" (
  "id" int NOT NULL AUTO_INCREMENT,
  "id_utilizador" int NOT NULL,
  "conteudo" text COLLATE utf8mb4_unicode_ci NOT NULL,
  "remetente" varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  "data_envio" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("id"),
  KEY "id_utilizador" ("id_utilizador"),
  CONSTRAINT "mensagem_ibfk_1" FOREIGN KEY ("id_utilizador") REFERENCES "utilizador" ("id")
);

-- DBprojetoFinal.produto definition

CREATE TABLE "produto" (
  "id" int NOT NULL AUTO_INCREMENT,
  "nome" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  "preco" int NOT NULL,
  "capa" varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  "fotos" varchar(800) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "estoque" int NOT NULL,
  "categoria" varchar(800) COLLATE utf8mb4_unicode_ci NOT NULL,
  "rate" int DEFAULT NULL,
  "descricao" varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "detalhes" varchar(2000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  "comentarios" varchar(4000) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY ("id")
);


-- DBprojetoFinal.utilizador definition

CREATE TABLE "utilizador" (
  "id" int NOT NULL AUTO_INCREMENT,
  "nome" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  "email" varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  "palavra_passe" varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  "grupo" int NOT NULL,
  PRIMARY KEY ("id")
);