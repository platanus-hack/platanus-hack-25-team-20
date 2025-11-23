import { Router } from 'express';
import { refreshPostings } from '$controllers/jobOfferingsController';

const router = Router();

router.post('/', refreshPostings);

export default router;
