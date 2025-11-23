import type { Request, Response, NextFunction } from 'express';
import type { JobOffering } from 'src/types/jobOffering';
import { linkedinScrapper } from '$scrappers';
import { getTranslator } from '../locale';

export const refreshPostings = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const { area, location, language = null } = req.body;
    const t = getTranslator(language);
    const jobs: JobOffering[] = await linkedinScrapper.getJobs(
      area,
      location,
      t,
    );
    res.status(200).json(jobs);
  } catch (error) {
    next(error);
  }
};
