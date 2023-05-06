create table if not exists api_monitor_record
(
    id               bigint    default nextval('demo.api_monitor_record_id_seq'::regclass) not null
        primary key,
    create_by        varchar(255),
    create_time      timestamp default CURRENT_TIMESTAMP,
    update_by        varchar(255),
    update_time      timestamp default CURRENT_TIMESTAMP,
    method           varchar(255),
    request_url      text,
    service          varchar(255),
    api              varchar(255),
    app              varchar(255),
    path             text,
    request_body     text,
    request_headers  text,
    response_body    text,
    response_headers text,
    scenario_name    varchar(255),
    status_code      integer                                                               not null
);
