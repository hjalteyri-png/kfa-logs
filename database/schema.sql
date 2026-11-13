-- Kveldúlfur Logs — normalized, source-aware performance database (PostgreSQL)
-- Schema v0.1. This is a design foundation, not a deployed database.
-- Source files are preserved and referenced by import batches.
create table if not exists data_sources (
  id bigint generated always as identity primary key,
  slug text not null unique,
  display_name text not null,
  homepage text,
  license text,
  import_notes text
);

create table if not exists import_batches (
  id bigint generated always as identity primary key,
  source_id bigint not null references data_sources(id),
  imported_at timestamptz not null default now(),
  source_version text,
  source_url text,
  source_checksum text,
  raw_rows bigint,
  metadata jsonb not null default '{}'::jsonb
);

create table if not exists athletes (
  id bigint generated always as identity primary key,
  display_name text not null,
  created_at timestamptz not null default now()
);

-- Do not merge same-name athletes automatically across data sources.
create table if not exists athlete_source_identities (
  id bigint generated always as identity primary key,
  athlete_id bigint not null references athletes(id),
  source_id bigint not null references data_sources(id),
  source_athlete_key text not null,
  source_display_name text not null,
  unique(source_id,source_athlete_key)
);

create table if not exists disciplines (
  id bigint generated always as identity primary key,
  slug text not null unique,
  name text not null
);

create table if not exists classes (
  id bigint generated always as identity primary key,
  discipline_id bigint not null references disciplines(id),
  slug text not null,
  name text not null,
  unique(discipline_id,slug)
);

create table if not exists feats (
  id bigint generated always as identity primary key,
  class_id bigint not null references classes(id),
  slug text not null,
  name text not null,
  unit text not null,
  better_direction text not null check(better_direction in ('higher','lower')),
  unique(class_id,slug)
);

create table if not exists rulesets (
  id bigint generated always as identity primary key,
  source_id bigint references data_sources(id),
  name text not null,
  version text,
  definition jsonb not null default '{}'::jsonb
);

create table if not exists events (
  id bigint generated always as identity primary key,
  source_id bigint references data_sources(id),
  source_event_key text,
  name text not null,
  starts_on date,
  location text,
  unique(source_id,source_event_key)
);

create table if not exists performances (
  id bigint generated always as identity primary key,
  athlete_id bigint not null references athletes(id),
  source_identity_id bigint references athlete_source_identities(id),
  source_id bigint not null references data_sources(id),
  import_batch_id bigint references import_batches(id),
  source_performance_key text not null,
  feat_id bigint not null references feats(id),
  ruleset_id bigint references rulesets(id),
  event_id bigint references events(id),
  performed_on date,
  value numeric not null,
  unit text not null,
  context jsonb not null default '{}'::jsonb,
  evidence jsonb not null default '{}'::jsonb,
  verification_status text not null default 'source_reported'
    check(verification_status in ('source_reported','self_reported','reviewed','official')),
  visibility text not null default 'public'
    check(visibility in ('public','unlisted','private')),
  raw_record jsonb,
  created_at timestamptz not null default now(),
  unique(source_id,source_performance_key)
);
create index if not exists performances_feat_value_idx on performances(feat_id,value);
create index if not exists performances_athlete_date_idx on performances(athlete_id,performed_on desc);
create index if not exists performances_context_idx on performances using gin(context);

-- Ranking cohorts must specify feat/ruleset/conditions, never silently mix categories.
create table if not exists ranking_definitions (
  id bigint generated always as identity primary key,
  slug text not null unique,
  feat_id bigint not null references feats(id),
  ruleset_id bigint references rulesets(id),
  cohort_filter jsonb not null default '{}'::jsonb,
  ranking_method text not null default 'absolute',
  version integer not null default 1
);
