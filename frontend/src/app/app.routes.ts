import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: '',
        loadComponent: () => import('./features/home/home.component').then(m => m.HomeComponent)
    },
    {
        path: 'resume',
        loadComponent: () => import('./features/resume/resume.component').then(m => m.ResumeComponent)
    },
    {
        path: 'document',
        loadComponent: () => import('./features/document/document.component').then(m => m.DocumentComponent)
    },
    {
        path: 'research',
        loadComponent: () => import('./features/research/research.component').then(m => m.ResearchComponent)
    },
    {
        path: 'creative',
        loadComponent: () => import('./features/creative/creative.component').then(m => m.CreativeComponent)
    },
    {
        path: 'email',
        loadComponent: () => import('./features/email/email.component').then(m => m.EmailComponent)
    },
    {
        path: 'social-media',
        loadComponent: () => import('./features/social-media/social-media.component').then(m => m.SocialMediaComponent)
    },
    {
        path: 'login',
        loadComponent: () => import('./features/auth/login.component').then(m => m.LoginComponent)
    },
    {
        path: 'register',
        loadComponent: () => import('./features/auth/register.component').then(m => m.RegisterComponent)
    },
    {
        path: 'dashboard',
        loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent)
    },
    {
        path: '**',
        redirectTo: 'dashboard'
    }
];
