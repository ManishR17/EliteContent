import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
    selector: 'app-home',
    standalone: true,
    imports: [CommonModule, RouterLink],
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css']
})
export class HomeComponent {
    contentTypes = [
        {
            icon: '📄',
            title: 'Resume Builder',
            description: 'Create ATS-optimized resumes tailored to specific job descriptions.',
            route: '/resume'
        },
        {
            icon: '📝',
            title: 'Document Generator',
            description: 'Generate professional business documents, proposals, and reports.',
            route: '/document'
        },
        {
            icon: '🎓',
            title: 'Research Paper',
            description: 'Draft academic papers with proper citations and structured arguments.',
            route: '/research'
        },
        {
            icon: '🎨',
            title: 'Creative Writing',
            description: 'Craft compelling stories, scripts, and creative content with AI assistance.',
            route: '/creative'
        },
        {
            icon: '📧',
            title: 'Email Writer',
            description: 'Generate professional emails for any occasion with AI assistance.',
            route: '/email'
        },
        {
            icon: '📱',
            title: 'Social Media',
            description: 'Create engaging social media posts and content with AI assistance.',
            route: '/social-media'
        }
    ];
}
