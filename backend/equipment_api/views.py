"""
Views for Chemical Equipment Visualizer API
"""
import os
import pandas as pd
from io import BytesIO
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import FileResponse, JsonResponse
from django.db.models import Count

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from .models import EquipmentDataset, Equipment
from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer,
    EquipmentDatasetSerializer,
    DatasetSummarySerializer,
    EquipmentSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user and return token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logout user by deleting token"""
    try:
        request.user.auth_token.delete()
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current user details"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Upload and process CSV file"""
    if 'file' not in request.FILES:
        return Response({
            'error': 'No file provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    # Validate file extension
    if not file.name.endswith('.csv'):
        return Response({
            'error': 'Only CSV files are allowed'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return Response({
                'error': f'Missing required columns: {", ".join(missing_columns)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Clean data
        df = df.dropna()
        
        # Calculate statistics
        total_equipment = len(df)
        avg_flowrate = df['Flowrate'].mean()
        avg_pressure = df['Pressure'].mean()
        avg_temperature = df['Temperature'].mean()
        
        # Save file
        upload_dir = settings.UPLOAD_DIR
        filename = f"{request.user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.name}"
        file_path = os.path.join(upload_dir, filename)
        
        # Save uploaded file
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Create dataset record
        dataset = EquipmentDataset.objects.create(
            user=request.user,
            filename=file.name,
            file_path=file_path,
            total_equipment=total_equipment,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature
        )
        
        # Create equipment records
        equipment_objects = []
        for _, row in df.iterrows():
            equipment_objects.append(Equipment(
                dataset=dataset,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            ))
        
        Equipment.objects.bulk_create(equipment_objects)
        
        # Maintain only last 5 datasets per user
        user_datasets = EquipmentDataset.objects.filter(user=request.user).order_by('-upload_date')
        if user_datasets.count() > 5:
            old_datasets = user_datasets[5:]
            for old_dataset in old_datasets:
                # Delete associated file
                if os.path.exists(old_dataset.file_path):
                    os.remove(old_dataset.file_path)
                old_dataset.delete()
        
        # Return dataset with equipment
        serializer = EquipmentDatasetSerializer(dataset)
        return Response({
            'message': 'File uploaded successfully',
            'dataset': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Error processing file: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_summary(request, dataset_id):
    """Get summary statistics for a specific dataset"""
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id, user=request.user)
        
        # Get equipment type distribution
        equipment_types = Equipment.objects.filter(dataset=dataset).values('equipment_type').annotate(
            count=Count('equipment_type')
        )
        
        type_distribution = {item['equipment_type']: item['count'] for item in equipment_types}
        
        serializer = EquipmentDatasetSerializer(dataset)
        
        return Response({
            'dataset': serializer.data,
            'type_distribution': type_distribution
        }, status=status.HTTP_200_OK)
        
    except EquipmentDataset.DoesNotExist:
        return Response({
            'error': 'Dataset not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_datasets(request):
    """List all datasets for current user"""
    datasets = EquipmentDataset.objects.filter(user=request.user)
    serializer = DatasetSummarySerializer(datasets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, dataset_id):
    """Delete a specific dataset"""
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id, user=request.user)
        
        # Delete associated file
        if os.path.exists(dataset.file_path):
            os.remove(dataset.file_path)
        
        dataset.delete()
        
        return Response({
            'message': 'Dataset deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except EquipmentDataset.DoesNotExist:
        return Response({
            'error': 'Dataset not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request, dataset_id):
    """Generate PDF report for a dataset"""
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id, user=request.user)
        equipment_list = Equipment.objects.filter(dataset=dataset)
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a365d'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2d3748'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        title = Paragraph("Chemical Equipment Analysis Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Report Info
        report_info = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Dataset:', dataset.filename],
            ['Upload Date:', dataset.upload_date.strftime('%Y-%m-%d %H:%M:%S')],
            ['Generated By:', request.user.username],
        ]
        
        info_table = Table(report_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary Statistics
        elements.append(Paragraph("Summary Statistics", heading_style))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Equipment', str(dataset.total_equipment)],
            ['Average Flowrate', f'{dataset.avg_flowrate:.2f}'],
            ['Average Pressure', f'{dataset.avg_pressure:.2f}'],
            ['Average Temperature', f'{dataset.avg_temperature:.2f}'],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Equipment Type Distribution
        equipment_types = Equipment.objects.filter(dataset=dataset).values('equipment_type').annotate(
            count=Count('equipment_type')
        ).order_by('-count')
        
        elements.append(Paragraph("Equipment Type Distribution", heading_style))
        
        type_data = [['Equipment Type', 'Count', 'Percentage']]
        for item in equipment_types:
            percentage = (item['count'] / dataset.total_equipment) * 100
            type_data.append([
                item['equipment_type'],
                str(item['count']),
                f'{percentage:.1f}%'
            ])
        
        type_table = Table(type_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(type_table)
        elements.append(PageBreak())
        
        # Equipment Details
        elements.append(Paragraph("Equipment Details", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        equipment_data = [['Name', 'Type', 'Flow', 'Press', 'Temp']]
        for eq in equipment_list:
            equipment_data.append([
                eq.equipment_name[:20],
                eq.equipment_type[:15],
                f'{eq.flowrate:.1f}',
                f'{eq.pressure:.1f}',
                f'{eq.temperature:.1f}'
            ])
        
        equipment_table = Table(equipment_data, colWidths=[2.2*inch, 1.8*inch, 0.9*inch, 0.9*inch, 0.9*inch])
        equipment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(equipment_table)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF value
        pdf = buffer.getvalue()
        buffer.close()
        
        # Save to reports directory
        report_filename = f"report_{dataset.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        report_path = os.path.join(settings.REPORTS_DIR, report_filename)
        
        with open(report_path, 'wb') as f:
            f.write(pdf)
        
        # Return as download
        response = FileResponse(open(report_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{report_filename}"'
        
        return response
        
    except EquipmentDataset.DoesNotExist:
        return Response({
            'error': 'Dataset not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Error generating PDF: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_statistics(request):
    """Get overall statistics for current user"""
    total_datasets = EquipmentDataset.objects.filter(user=request.user).count()
    total_equipment = Equipment.objects.filter(dataset__user=request.user).count()
    
    return Response({
        'total_datasets': total_datasets,
        'total_equipment': total_equipment,
        'username': request.user.username
    }, status=status.HTTP_200_OK)
