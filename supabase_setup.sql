-- Supabase > SQL Editor da RUN qiling
create table if not exists kv (k text primary key, v jsonb not null default '[]');
alter table kv enable row level security;  -- siyosat yo'q: faqat server (service_role) kira oladi
