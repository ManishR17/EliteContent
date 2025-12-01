import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-preview',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './preview.component.html',
    styleUrls: ['./preview.component.css']
})
export class PreviewComponent {
    @Input() content: string = '';
    @Input() type: 'resume' | 'document' | 'email' | 'social' | 'creative' = 'document';
    @Input() metadata: any = {}; // Extra data like subject, platform, etc.

    // Helper to format text with line breaks
    formatContent(text: string): string {
        return text ? text.replace(/\n/g, '<br>') : '';
    }
}
