// MFC1View.h : interface of the CMFC1View class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_MFC1VIEW_H__DF756434_0853_444C_9AB1_481B5B4925E5__INCLUDED_)
#define AFX_MFC1VIEW_H__DF756434_0853_444C_9AB1_481B5B4925E5__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000


class CMFC1View : public CView
{
protected: // create from serialization only
	CMFC1View();
	DECLARE_DYNCREATE(CMFC1View)

// Attributes
public:
	CMFC1Doc* GetDocument();

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMFC1View)
	public:
	virtual void OnDraw(CDC* pDC);  // overridden to draw this view
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
	protected:
	virtual BOOL OnPreparePrinting(CPrintInfo* pInfo);
	virtual void OnBeginPrinting(CDC* pDC, CPrintInfo* pInfo);
	virtual void OnEndPrinting(CDC* pDC, CPrintInfo* pInfo);
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CMFC1View();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	//{{AFX_MSG(CMFC1View)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

#ifndef _DEBUG  // debug version in MFC1View.cpp
inline CMFC1Doc* CMFC1View::GetDocument()
   { return (CMFC1Doc*)m_pDocument; }
#endif

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_MFC1VIEW_H__DF756434_0853_444C_9AB1_481B5B4925E5__INCLUDED_)
