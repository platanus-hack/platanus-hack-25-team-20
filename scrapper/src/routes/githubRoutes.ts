import { Router } from 'express';
import { getUserData } from '$controllers/githubIntegrationController';

const router = Router();

router.get('/user/:username', getUserData);

export default router;
