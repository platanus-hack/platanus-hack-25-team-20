import { App } from "octokit"

export const githubClient = {
  getUserData: async (
    username: string,
  ): Promise<Record<string, number>> => {
    const octokit = await githubClient.generateClient();

    const response = await octokit.request('GET /users/{username}/repos', {
      username,
      headers: {
        'X-GitHub-Api-Version': '2022-11-28'
      }
    })
    const repos: Record<string, number> = {}
    response.data.forEach((repo: any) => {
      if(!!repo.language) {
        repos[repo.language] = (repos[repo.language as string] || 0) + 1
      }
    })

    return repos
  },

  generateClient: async() => {
    const { GITHUB_APP_ID, GITHUB_PRIVATE_KEY, GITHUB_INSTALLATION_ID } = process.env;

    if (!GITHUB_APP_ID || !GITHUB_PRIVATE_KEY || !GITHUB_INSTALLATION_ID) {
      throw new Error("Missing Github App credentials");
    }

    const app = new App({
      appId: GITHUB_APP_ID,
      privateKey: GITHUB_PRIVATE_KEY,
    });
    
    const octokit = await app.getInstallationOctokit(parseInt(GITHUB_INSTALLATION_ID, 10))
    return octokit
  }
};
