import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../core/services/api.service';

@Component({
    selector: 'app-dashboard',
    standalone: true,
    imports: [CommonModule, RouterModule],
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
    stats: any = {
        total_generated: 0,
        collections: {
            resumes: 0,
            documents: 0,
            emails: 0,
            social: 0,
            creative: 0
        },
        system_status: 'checking...'
    };

    recentActivity = [
        { type: 'Resume', title: 'Software Engineer Resume', date: '2 hours ago', status: 'Completed' },
        { type: 'Research', title: 'AI Trends 2025', date: '5 hours ago', status: 'Cached' },
        { type: 'Social', title: 'LinkedIn Post', date: '1 day ago', status: 'Completed' }
    ];

    quickActions = [
        { title: 'New Resume', icon: '📄', route: '/resume', description: 'ATS-optimized resume' },
        { title: 'Research Topic', icon: '🔍', route: '/research', description: 'Deep dive with RAG' },
        { title: 'Write Document', icon: '📝', route: '/document', description: 'Proposals & reports' },
        { title: 'Social Post', icon: '📱', route: '/social-media', description: 'Engaging content' },
        { title: 'Draft Email', icon: '✉️', route: '/email', description: 'Professional emails' },
        { title: 'Creative', icon: '🎨', route: '/creative', description: 'Stories & blogs' }
    ];

    constructor(private apiService: ApiService) { }

    ngOnInit() {
        this.loadStats();
    }

    loadStats() {
        this.apiService.getDashboardStats().subscribe({
            next: (data) => {
                this.stats = data;
            },
            error: (err) => {
                console.error('Failed to load stats', err);
                this.stats.system_status = 'offline';
            }
        });
    }
}
