with remote_job_skills as(
select skill_id,count(*) as skill_count
from skills_job_dim
inner join job_postings_fact on skills_job_dim.job_id=job_postings_fact.job_id
where job_postings_fact.job_work_from_home=true AND job_postings_fact.job_title_short='Data Analyst'
group by skill_id
)
select skills,skill_count from remote_job_skills
inner join skills_dim on remote_job_skills.skill_id=skills_dim.skill_id
order by skill_count desc
limit 5