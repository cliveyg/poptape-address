--
-- PostgreSQL database dump
--

-- Dumped from database version 11.3
-- Dumped by pg_dump version 11.3

-- SET statement_timeout = 0;
-- SET lock_timeout = 0;
-- SET idle_in_transaction_session_timeout = 0;
-- SET client_encoding = 'UTF8';
-- SET standard_conforming_strings = on;
-- SELECT pg_catalog.set_config('search_path', '', false);
-- SET check_function_bodies = false;
-- SET xmloption = content;
-- SET client_min_messages = warning;
-- SET row_security = off;

-- SET default_tablespace = '';

-- SET default_with_oids = false;

--
-- Name: address; Type: TABLE; Schema: public; Owner: poptape_address
--

CREATE TABLE public.address (
    id integer NOT NULL,
    address_id character varying(50) NOT NULL,
    public_id character varying(50) NOT NULL,
    house_name character varying(50),
    house_number character varying(50),
    address_line_1 character varying(150),
    address_line_2 character varying(150),
    address_line_3 character varying(150),
    state_region_county character varying(150),
    country_id integer,
    post_zip_code character varying(30),
    created timestamp without time zone NOT NULL
);


ALTER TABLE public.address OWNER TO poptape_address;

--
-- Name: address_id_seq; Type: SEQUENCE; Schema: public; Owner: poptape_address
--

CREATE SEQUENCE public.address_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.address_id_seq OWNER TO poptape_address;

--
-- Name: address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poptape_address
--

ALTER SEQUENCE public.address_id_seq OWNED BY public.address.id;


--
-- Name: country; Type: TABLE; Schema: public; Owner: poptape_address
--

CREATE TABLE public.country (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    iso_code character varying(3) NOT NULL
);


ALTER TABLE public.country OWNER TO poptape_address;

--
-- Name: country_id_seq; Type: SEQUENCE; Schema: public; Owner: poptape_address
--

CREATE SEQUENCE public.country_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.country_id_seq OWNER TO poptape_address;

--
-- Name: country_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: poptape_address
--

ALTER SEQUENCE public.country_id_seq OWNED BY public.country.id;


--
-- Name: address id; Type: DEFAULT; Schema: public; Owner: poptape_address
--

ALTER TABLE ONLY public.address ALTER COLUMN id SET DEFAULT nextval('public.address_id_seq'::regclass);


--
-- Name: country id; Type: DEFAULT; Schema: public; Owner: poptape_address
--

ALTER TABLE ONLY public.country ALTER COLUMN id SET DEFAULT nextval('public.country_id_seq'::regclass);


--
-- Name: address address_address_id_key; Type: CONSTRAINT; Schema: public; Owner: poptape_address
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_address_id_key UNIQUE (address_id);


--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: poptape_address
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (id);


--
-- Name: country country_iso_code_key; Type: CONSTRAINT; Schema: public; Owner: poptape_address
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_iso_code_key UNIQUE (iso_code);


--
-- Name: country country_name_key; Type: CONSTRAINT; Schema: public; Owner: poptape_address
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_name_key UNIQUE (name);


--
-- Name: country country_pkey; Type: CONSTRAINT; Schema: public; Owner: poptape_address
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (id);


--
-- Name: address address_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: poptape_address
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.country(id);


--
-- PostgreSQL database dump complete
--

