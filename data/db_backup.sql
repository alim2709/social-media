--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comments (
    id integer NOT NULL,
    content character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_blocked boolean NOT NULL,
    author_id integer NOT NULL,
    post_id integer NOT NULL,
    parent_id integer
);


ALTER TABLE public.comments OWNER TO postgres;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comments_id_seq OWNER TO postgres;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    title character varying NOT NULL,
    content character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_blocked boolean NOT NULL,
    author_id integer NOT NULL
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_id_seq OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_active boolean NOT NULL,
    auto_reply_enabled boolean NOT NULL,
    auto_reply_delay integer NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
8c684461d3f8
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comments (id, content, created_at, is_blocked, author_id, post_id, parent_id) FROM stdin;
1	Test comment content	2024-11-11 11:05:47.294652	f	1	1	\N
2	Test2 comment content	2024-11-11 11:05:55.690023	f	1	1	\N
3	Test3 comment content	2024-11-11 11:06:00.951146	f	1	1	\N
4	Test4 comment content	2024-11-11 11:06:10.996746	f	1	1	\N
5	Test6 comment content	2024-11-11 11:06:24.309444	f	1	2	\N
6	Test7 comment content	2024-11-11 11:06:28.979925	f	1	2	\N
7	Test8 comment content	2024-11-11 11:06:32.758873	f	1	2	\N
8	Test9 comment content	2024-11-11 11:06:42.589071	f	1	3	\N
9	Test10 comment content	2024-11-11 11:06:49.143923	f	1	3	\N
10	Test11 comment content	2024-11-11 11:06:53.650011	f	1	3	\N
11	Test comment content from test_user	2024-11-11 11:10:09.035421	f	3	1	\N
12	Test2 comment content from test_user	2024-11-11 11:10:16.409084	f	3	1	\N
13	Test3 comment content from test_user	2024-11-11 11:10:20.915087	f	3	1	\N
14	Test4 comment content from test_user	2024-11-11 11:10:31.973641	f	3	2	\N
15	Test5 comment content from test_user	2024-11-11 11:10:36.684051	f	3	2	\N
16	Test6 comment content from test_user	2024-11-11 11:10:40.165836	f	3	2	\N
17	Test7 comment content from test_user	2024-11-11 11:10:50.816148	f	3	4	\N
18	Test8 comment content from test_user	2024-11-11 11:10:56.142426	f	3	4	\N
19	Test9 comment content from test_user	2024-11-11 11:11:03.92476	f	3	4	\N
20	Test10 comment content from test_user	2024-11-11 11:11:19.284878	f	3	6	\N
21	Test11 comment content from test_user	2024-11-11 11:11:27.886803	f	3	6	\N
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posts (id, title, content, created_at, is_blocked, author_id) FROM stdin;
1	Test post title	Test content title	2024-11-11 11:04:19.84514	f	1
2	Test2 post title	Test2 content title	2024-11-11 11:04:31.638898	f	1
3	Test3 post title	Test3 content title	2024-11-11 11:04:40.525668	f	1
4	Test post title from test_user	Test content title from test_user	2024-11-11 11:09:21.519911	f	3
5	Test1 post title from test_user	Test2 content title from test_user	2024-11-11 11:09:31.760156	f	3
6	Test2 post title from test_user	Test3 content title from test_user	2024-11-11 11:09:39.305144	f	3
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, hashed_password, is_active, auto_reply_enabled, auto_reply_delay) FROM stdin;
1	alim	alimselemetow@gmail.com	$2b$12$XkNrcSivWGLYt/.ieOgYd.ZYlmJy7RT6hgN/SEYLPmBB86cQj8sDe	t	f	10
2	string	user@example.com	$2b$12$rFcC1.BbZ3DfE0tYjrUW6uNQDcbLVB/PcCUBWkhq5x/TUSoToWLZy	t	f	10
3	test_user	test@test.com	$2b$12$Zfqm.bNwC9Ke9yc2YkTqTeIouz5y9j3xKUv0u1KXcId4XHxedYsg.	t	f	10
\.


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comments_id_seq', 21, true);


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.posts_id_seq', 6, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: posts posts_content_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_content_key UNIQUE (content);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: posts posts_title_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_title_key UNIQUE (title);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_hashed_password_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_hashed_password_key UNIQUE (hashed_password);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_comments_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_comments_id ON public.comments USING btree (id);


--
-- Name: ix_posts_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_posts_id ON public.posts USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: comments comments_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- Name: comments comments_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.comments(id);


--
-- Name: comments comments_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id);


--
-- Name: posts posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

