import type { JobOffering } from 'src/types/jobOffering';
import ky from 'ky';
import * as cheerio from 'cheerio';
import type { Translator } from '$locale';

export const linkedinScrapper = {
  getJobs: async (
    area: string,
    location: string,
    t: Translator,
  ): Promise<JobOffering[]> => {
    const domain = t('linkedin.domain');
    const baseUrl = `https://${domain}.linkedin.com`;

    const jobsHTML = await ky
      .get(`${baseUrl}/jobs/search`, {
        searchParams: {
          keywords: area,
          location,
          trk: 'public_jobs_jobs-search-bar_search-submit',
        },
      })
      .text();

    const $ = cheerio.load(jobsHTML);

    const jobs: JobOffering[] = [];

    $('.jobs-search__results-list > li').each((_, element) => {
      const card = $(element).find('div.base-card');
      const entityUrn = card.attr('data-entity-urn');
      const uid = entityUrn?.split(':').pop() || '';

      const role_name = card.find('.base-search-card__title').text().trim();
      const company_name = card
        .find('.base-search-card__subtitle')
        .text()
        .trim();
      const locationText = card
        .find('.job-search-card__location')
        .text()
        .trim();
      const postDateStr = card
        .find('.job-search-card__listdate')
        .attr('datetime');
      const post_date = postDateStr ? new Date(postDateStr) : new Date();
      const rawUrl = card.find('.base-card__full-link').attr('href') || '';
      const url = rawUrl.split('?')[0] || rawUrl;
      jobs.push({
        uid,
        company_name,
        role_name,
        location: locationText,
        post_date,
        description: '',
        api_url: `${baseUrl}/jobs-guest/jobs/api/jobPosting/${uid}?trackingId=`,
        salary: null,
        work_mode: null,
        extra_data: {},
        type: null,
        url,
        keyword: area,
      });
    });

    for (const job of jobs) {
      try {
        // Random delay between 2 and 4 seconds
        const delay = Math.floor(Math.random() * 2000) + 2000;
        await new Promise((resolve) => setTimeout(resolve, delay));

        const jobResponse = await ky.get(job.api_url as string).text();
        const $$ = cheerio.load(jobResponse);

        const salaryText = $$('.salary.compensation__salary').text().trim();
        job.salary = salaryText || null;

        job.description =
          $$('.show-more-less-html__markup').html()?.trim() || '';

        const criteria: Record<string, string> = {};

        $$('.description__job-criteria-item').each((_, element) => {
          const subheader = $$(element)
            .find('.description__job-criteria-subheader')
            .text()
            .trim();
          const text = $$(element)
            .find('.description__job-criteria-text')
            .text()
            .trim();

          if (subheader.includes(t('linkedin.jobFields.seniority'))) {
            criteria.seniority = text;
          } else if (subheader.includes(t('linkedin.jobFields.work_mode'))) {
            job.work_mode = text;
          } else if (
            subheader.includes(t('linkedin.jobFields.responsability'))
          ) {
            criteria.responsability = text;
          } else if (subheader.includes(t('linkedin.jobFields.sectors'))) {
            job.sectors = text;
          }
        });

        job.extra_data = {
          ...job.extra_data,
          seniority: criteria['seniority'],
          responsability: criteria['responsability'],
        };
      } catch (error) {
        console.error(`Failed to fetch details for job ${job.uid}:`, error);
      }
    }

    return jobs;
  },
};
