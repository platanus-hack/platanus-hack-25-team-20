import express from 'express';
import jobOfferingRoutes from '$routes/jobOfferingRoutes';
import githubRoutes from '$routes/githubRoutes';
import { errorHandler } from '$middlewares/errorHandler';

const app = express();

app.use(express.json());

// Routes
app.use('/api/postings', jobOfferingRoutes);
app.use('/api/github', githubRoutes);

// Global error handler (should be after routes)
app.use(errorHandler);

export default app;
