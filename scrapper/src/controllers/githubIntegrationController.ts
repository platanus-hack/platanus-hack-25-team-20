import type { Request, Response, NextFunction } from 'express';
import { githubClient } from '$scrappers';

export const getUserData = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const { username } = req.params;
    const profile = await githubClient.getUserData(username as string);
    res.status(200).json(profile);
  } catch (error) {
    next(error);
  }
};
