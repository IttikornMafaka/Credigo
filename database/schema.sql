--
-- PostgreSQL database dump
--

\restrict sX1MHC4ebjiYeQZ50FZJw0rEZvilxBOdmN793gU1cuTZTwx3YhIp6uxg8DIYAVj

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.4

-- Started on 2026-11-02 13:25:52

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
-- TOC entry 223 (class 1259 OID 16513)
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    account_id uuid DEFAULT gen_random_uuid() NOT NULL,
    customer_id uuid NOT NULL,
    account_number character varying(30),
    bank_name character varying(100),
    account_type character varying(50),
    balance numeric(15,2),
    account_status character varying(30),
    opened_at date
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16650)
-- Name: credit_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.credit_history (
    credit_id bigint NOT NULL,
    customer_id uuid NOT NULL,
    credit_score integer,
    total_debt numeric(15,2),
    credit_utilization numeric(5,2),
    recorded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.credit_history OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16649)
-- Name: credit_history_credit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.credit_history ALTER COLUMN credit_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.credit_history_credit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 16426)
-- Name: customers_detail; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers_detail (
    customer_id uuid DEFAULT gen_random_uuid() NOT NULL,
    national_id character varying(13) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    date_of_birth date NOT NULL,
    gender character varying(20) NOT NULL,
    phone_number character varying(20) NOT NULL,
    email text NOT NULL,
    address text NOT NULL,
    marital_status character varying(20),
    education character varying(50),
    update_at timestamp(6) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT national_id_length_check CHECK (((national_id)::text ~ '^[0-9]{13}$'::text))
);


ALTER TABLE public.customers_detail OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16492)
-- Name: employment_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employment_records (
    employment_id uuid DEFAULT gen_random_uuid() NOT NULL,
    customer_id uuid NOT NULL,
    company_name character varying(255),
    job_title character varying(100),
    employment_type character varying(50),
    monthly_income numeric(15,2),
    employment_start_date date
);


ALTER TABLE public.employment_records OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16563)
-- Name: loans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loans (
    loan_id bigint NOT NULL,
    customer_id uuid NOT NULL,
    loan_amount numeric(15,2),
    interest_rate numeric(5,2),
    loan_term integer,
    loan_status character varying(30),
    application_date date
);


ALTER TABLE public.loans OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16562)
-- Name: loans_loan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.loans ALTER COLUMN loan_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.loans_loan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 227 (class 1259 OID 16622)
-- Name: repayment_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.repayment_records (
    repayment_id bigint NOT NULL,
    customer_id uuid NOT NULL,
    loan_id bigint NOT NULL,
    payment_amount numeric(15,2),
    due_date date,
    payment_date date,
    payment_status character varying(30)
);


ALTER TABLE public.repayment_records OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16621)
-- Name: repayment_records_repayment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.repayment_records ALTER COLUMN repayment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.repayment_records_repayment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4893 (class 2606 OID 16520)
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (account_id);


--
-- TOC entry 4899 (class 2606 OID 16657)
-- Name: credit_history credit_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_history
    ADD CONSTRAINT credit_history_pkey PRIMARY KEY (credit_id);


--
-- TOC entry 4887 (class 2606 OID 16444)
-- Name: customers_detail customers_detail_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers_detail
    ADD CONSTRAINT customers_detail_pkey PRIMARY KEY (customer_id);


--
-- TOC entry 4891 (class 2606 OID 16499)
-- Name: employment_records employment_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employment_records
    ADD CONSTRAINT employment_records_pkey PRIMARY KEY (employment_id);


--
-- TOC entry 4895 (class 2606 OID 16569)
-- Name: loans loans_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT loans_pkey PRIMARY KEY (loan_id);


--
-- TOC entry 4889 (class 2606 OID 16458)
-- Name: customers_detail national_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers_detail
    ADD CONSTRAINT national_id_unique UNIQUE (national_id);


--
-- TOC entry 4897 (class 2606 OID 16629)
-- Name: repayment_records repayment_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repayment_records
    ADD CONSTRAINT repayment_records_pkey PRIMARY KEY (repayment_id);


--
-- TOC entry 4900 (class 2606 OID 16500)
-- Name: employment_records employment_records_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employment_records
    ADD CONSTRAINT employment_records_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers_detail(customer_id);


--
-- TOC entry 4901 (class 2606 OID 16521)
-- Name: accounts fk_customer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES public.customers_detail(customer_id);


--
-- TOC entry 4905 (class 2606 OID 16658)
-- Name: credit_history fk_customer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credit_history
    ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES public.customers_detail(customer_id);


--
-- TOC entry 4902 (class 2606 OID 16570)
-- Name: loans fk_customer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loans
    ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES public.customers_detail(customer_id);


--
-- TOC entry 4903 (class 2606 OID 16630)
-- Name: repayment_records fk_customer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repayment_records
    ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES public.customers_detail(customer_id);


--
-- TOC entry 4904 (class 2606 OID 16635)
-- Name: repayment_records fk_loan; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repayment_records
    ADD CONSTRAINT fk_loan FOREIGN KEY (loan_id) REFERENCES public.loans(loan_id);


-- Completed on 2026-11-02 13:25:52

--
-- PostgreSQL database dump complete
--

\unrestrict sX1MHC4ebjiYeQZ50FZJw0rEZvilxBOdmN793gU1cuTZTwx3YhIp6uxg8DIYAVj

