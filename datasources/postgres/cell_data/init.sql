--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

-- Started on 2021-11-07 09:28:31

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 204 (class 1259 OID 147475)
-- Name: abuse_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.abuse_metadata (
    temp numeric,
    thickness numeric,
    v_init numeric,
    indentor numeric,
    nail_speed numeric,
    cell_id character varying(100)
);


ALTER TABLE public.abuse_metadata OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 147481)
-- Name: abuse_timeseries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.abuse_timeseries (
    axial_d numeric,
    axial_f numeric,
    v numeric,
    norm_d numeric,
    strain numeric,
    temp_1 numeric,
    temp_2 numeric,
    temp_3 numeric,
    temp_4 numeric,
    temp_5 numeric,
    temp_6 numeric,
    test_time numeric,
    cell_id character varying(100)
);


ALTER TABLE public.abuse_timeseries OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 49165)
-- Name: cell_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cell_metadata (
    cathode character varying(50),
    anode character varying(50),
    source character varying(50),
    ah numeric,
    form_factor character varying(50),
    cell_id character varying(100),
    test character varying(50),
    tester character varying(50)
);


ALTER TABLE public.cell_metadata OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 90112)
-- Name: cycle_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cycle_metadata (
    temp numeric,
    soc_max numeric,
    soc_min numeric,
    v_max numeric,
    v_min numeric,
    crate_c numeric,
    crate_d numeric,
    cell_id character varying(100)
);


ALTER TABLE public.cycle_metadata OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 49153)
-- Name: cycle_stats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cycle_stats (
    v_max numeric,
    v_min numeric,
    ah_c numeric,
    ah_d numeric,
    e_c numeric,
    e_d numeric,
    i_max numeric,
    i_min numeric,
    v_c_mean numeric,
    v_d_mean numeric,
    e_eff numeric,
    ah_eff numeric,
    cycle_index numeric,
    test_time numeric,
    cell_id character varying(100)
);


ALTER TABLE public.cycle_stats OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 49159)
-- Name: cycle_timeseries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cycle_timeseries (
    i numeric,
    v numeric,
    ah_c numeric,
    ah_d numeric,
    e_c numeric,
    e_d numeric,
    temp_1 numeric,
    temp_2 numeric,
    cycle_time numeric,
    date_time timestamp without time zone,
    cycle_index numeric,
    test_time numeric,
    cell_id character varying(100)
);


ALTER TABLE public.cycle_timeseries OWNER TO postgres;

--
-- TOC entry 2878 (class 1259 OID 155667)
-- Name: idx_abuse_metadata_cell_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_abuse_metadata_cell_id ON public.abuse_metadata USING btree (cell_id);


--
-- TOC entry 2879 (class 1259 OID 155668)
-- Name: idx_abuse_timeseries_cell_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_abuse_timeseries_cell_id ON public.abuse_timeseries USING btree (cell_id);


--
-- TOC entry 2876 (class 1259 OID 49178)
-- Name: idx_cell_metadata_cell_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cell_metadata_cell_id ON public.cell_metadata USING btree (cell_id);


--
-- TOC entry 2877 (class 1259 OID 90118)
-- Name: idx_cycle_metadata_cell_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cycle_metadata_cell_id ON public.cycle_metadata USING btree (cell_id);


--
-- TOC entry 2874 (class 1259 OID 49176)
-- Name: idx_cycle_stats_cell_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cycle_stats_cell_id ON public.cycle_stats USING btree (cell_id);


--
-- TOC entry 2875 (class 1259 OID 49177)
-- Name: idx_cycle_timeseries_cell_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cycle_timeseries_cell_id ON public.cycle_timeseries USING btree (cell_id);


-- Completed on 2021-11-07 09:28:31

--
-- PostgreSQL database dump complete
--

